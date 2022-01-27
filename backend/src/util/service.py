import asyncio
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union, Any

import psutil
from fastapi import Request, WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK

from src.modules.fritz import Fritz, FritzStats
from src.modules.jelly import Jelly
from src.modules.kvm import KVM, State
from src.modules.plex import Plex
from src.modules.sabnzbd import Sabnzbd
from src.modules.storage import Storage
from src.modules.system import SystemStats
from src.util.observer import Observer


def uptime() -> int:
    return round(
        (datetime.now() -
         datetime.fromtimestamp(psutil.boot_time())).total_seconds())


def convert_to_mbit(value) -> int:
    return value / 1024. / 1024. / 1024. * 8


def shutdown() -> Dict[str, Union[bool, str]]:
    cmd = subprocess.check_output(['sudo', 'shutdown']).strip()
    return {"success": True, "message": cmd}


def reboot() -> Dict[str, Union[bool, str]]:
    cmd = subprocess.check_output(['sudo', 'shutdown', '-r']).strip()
    return {"success": True, "message": cmd}


class Service:
    config: Dict[str, str]
    kvm: KVM
    jelly: Jelly
    plex: Plex
    nzb: Sabnzbd
    fritz: Fritz
    system_stats: SystemStats
    fritz_stats: FritzStats
    storage: Storage

    def __init__(self, config) -> None:
        self.config = config
        self.kvm = KVM()
        self.jelly = Jelly(config["JELLY"])
        self.plex = Plex(config["PLEX"])
        self.nzb = Sabnzbd(config["NZB"])
        self.fritz = Fritz(config["FRITZ"])
        self.system_stats = SystemStats()
        self.fritz_stats = FritzStats(self.fritz)
        self.storage = Storage(config["STORAGE"])

    def active_services(self) -> Dict[str, Union[bool, str, Dict]]:
        active_check = self.check_active()
        active = active_check[0]
        details = active_check[1]

        return {"result": active, "active": details}

    async def server_stats(self,
                           websocket: WebSocket,
                           rate: Optional[int] = 1):
        system_observer = Observer(self.system_stats)
        try:
            await websocket.accept()
            while True:
                await asyncio.sleep(rate)
                data = system_observer.value
                await websocket.send_json(data)

        except (WebSocketDisconnect, ConnectionClosedOK):
            await websocket.close()
            self.system_stats.unsubscribe(system_observer)
            print("System stats WebSocket disconnected")

    async def net_stats(self, websocket: WebSocket, rate: Optional[int] = 1):
        fritz_observer = Observer(self.fritz_stats)
        try:
            await websocket.accept()
            while True:
                await asyncio.sleep(rate)
                data = fritz_observer.value

                await websocket.send_json(data)

        except (WebSocketDisconnect, ConnectionClosedOK):
            await websocket.close()
            self.fritz_stats.unsubscribe(fritz_observer)
            print("Network stats WebSocket disconnected")

    def all_vms(self) -> Dict:
        vms = self.kvm.get_vms()
        sorted_vms = sorted(vms, key=lambda d: d['name'])
        response = {"result": []}
        for vm in sorted_vms:
            response["result"].append(vm)

        return response

    def active_vms(self) -> Dict[str, List]:
        vms = self.kvm.get_active()
        response = {"result": []}
        for vm in vms:
            response["result"].append({
                "name": vm[0],
                "state": vm[1],
            })

        return response

    async def edit_vm(self, domain, request: Request):
        data = await request.json()
        for k, v in data.items():
            if k == "memory":
                result = self.kvm.set_active_memory(domain, v)

                return {"result": result.status}
            elif k == "state":
                if v == "start" or v == "boot":
                    result = self.kvm.boot_vm(domain)
                    return {"result": result.status}
                elif v == "stop" or v == "shutdown":
                    result = self.kvm.shutdown_vm(domain)
                    return {"result": result.status}
                elif v == "destroy":
                    result = self.kvm.destroy_vm(domain)
                    return {"result": result.status}

            else:
                return {
                    "result": {
                        "success": False,
                        "message": f"'{k}' not implemented"
                    }
                }

    def vm_info(self, domain) -> Dict[str, State]:
        result = self.kvm.get_vm_info(domain)

        return {"result": result.status}

    def start_vm(self, domain: str) -> Dict[str, State]:
        result = self.kvm.boot_vm(domain)

        return {"result": result.status}

    def stop_vm(self, domain: str) -> Dict[str, State]:
        result = self.kvm.shutdown_vm(domain)

        return {"result": result.status}

    def check_active(self) -> Tuple[bool, Dict[str, bool]]:
        jelly_active = self.jelly.is_active()
        plex_active = self.plex.is_active()
        kvm_active = self.kvm.is_active()
        nzb_active = self.nzb.is_active()
        return (jelly_active and plex_active and kvm_active and nzb_active), {
            "jelly": jelly_active,
            "plex": plex_active,
            "nzb": nzb_active,
            "kvm": kvm_active
        }

    def get_external_ip(self) -> Dict[str, Dict[str, int]]:
        ext_ip = self.fritz.get_external_ip()
        return {"result": {'v4': ext_ip[0], 'v6': ext_ip[1]}}

    def get_max_bandwidth(self) -> Dict[str, Dict[str, int]]:
        bitrate = self.fritz.get_max_bandwidth()
        return {"result": {'up': bitrate[0], 'down': bitrate[1]}}

    def get_current_bandwidth(self) -> Dict[str, Dict[str, int]]:
        bitrate = self.fritz.get_current_bandwidth()
        return {"result": {'up': bitrate[0], 'down': bitrate[1]}}

    def fritz_info(self) -> Dict[str, Any]:
        max_bandwidth = self.fritz.get_max_bandwidth()
        ext_ip = self.fritz.get_external_ip()

        return {
            "result": {
                "net": {
                    "up": max_bandwidth[0],
                    "down": max_bandwidth[1]
                },
                "ip": {
                    "v4": ext_ip[0],
                    "v6": ext_ip[1]
                }
            }
        }

    def storage_usage(self) -> Dict[str, List[Dict[str, Any]]]:
        usage = self.storage.get_usage()

        return {"result": usage}
