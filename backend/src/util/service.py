import psutil
import asyncio
import subprocess
from typing import Dict, List, Optional, Tuple, Union
from fastapi import Request, WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK
from datetime import datetime
from modules.fritz import Fritz
from modules.jelly import Jelly
from modules.kvm import KVM, State
from modules.plex import Plex
from modules.sabnzbd import Sabnzbd


class Service:
    config: Dict[str, str]
    kvm: KVM
    jelly: Jelly
    plex: Plex
    nzb: Sabnzbd
    fritz: Fritz

    def __init__(self, config) -> None:
        self.config = config
        self.kvm = KVM()
        self.jelly = Jelly(config["JELLY"])
        self.plex = Plex(config["PLEX"])
        self.nzb = Sabnzbd(config["NZB"])
        self.fritz = Fritz(config["FRITZ"])

    def idle(self) -> Dict[str, Union[bool, str, Dict]]:
        idle_check = self.check_all_idle()
        idle = idle_check[0]
        details = idle_check[1]

        return {"result": idle, "idle": details}

    def uptime(self) -> int:
        return round(
            (datetime.now() -
             datetime.fromtimestamp(psutil.boot_time())).total_seconds())

    async def server_stats(self,
                           websocket: WebSocket,
                           rate: Optional[int] = 1):
        try:
            await websocket.accept()
            while True:
                await asyncio.sleep(rate)
                cpu_pct = psutil.cpu_percent()
                total, available, used, *_ = psutil.virtual_memory()
                netio = psutil.net_io_counters(pernic=True)
                await websocket.send_json({
                    "cpu": cpu_pct,
                    "net": {
                        "in": netio["enp5s0"].bytes_recv,
                        "out": netio["enp5s0"].bytes_sent
                    },
                    "memory": {
                        "total": total,
                        "used": used,
                        "free": available
                    }
                })

        except WebSocketDisconnect:
            websocket.close()
            print("WebSocket disconnected")
        except ConnectionClosedOK:
            print("WebSocket closed gracefully")

    async def net_stats(self, websocket: WebSocket, rate: Optional[int] = 1):
        try:
            await websocket.accept()
            while True:
                await asyncio.sleep(rate)

                await websocket.send_json({
                    "in":
                    self.fritz.get_current_bandwidth()[1],
                    "out":
                    self.fritz.get_current_bandwidth()[0]
                })

        except WebSocketDisconnect:
            websocket.close()
            print("WebSocket disconnected")
        except ConnectionClosedOK:
            print("WebSocket closed gracefully")

    def convert_to_mbit(value) -> int:
        return value / 1024. / 1024. / 1024. * 8

    def shutdown(self) -> Dict[str, Union[bool, str]]:
        cmd = subprocess.check_output(['sudo', 'shutdown']).strip()
        return {"success": True, "message": cmd}

    def reboot(self) -> Dict[str, Union[bool, str]]:
        cmd = subprocess.check_output(['sudo', 'shutdown', '-r']).strip()
        return {"success": True, "message": cmd}

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

    def check_all_idle(self) -> Tuple[bool, Dict[str, bool]]:
        jelly_idle = self.jelly.is_jelly_idle()
        plex_idle = self.plex.is_plex_idle()
        kvm_idle = self.kvm.is_kvm_idle()
        nzb_idle = self.nzb.is_nzb_idle()

        return (jelly_idle and plex_idle and kvm_idle and nzb_idle), {
            "jelly": jelly_idle,
            "plex": plex_idle,
            "nzb": nzb_idle,
            "kvm": kvm_idle
        }

    def get_external_ip(self) -> Dict[str, str]:
        ext_ip = self.fritz.get_external_ip()
        return {"result": {'v4': ext_ip[0], 'v6': ext_ip[1]}}

    def get_max_bandwidth(self) -> Dict[str, str]:
        bitrate = self.fritz.get_max_bandwidth()
        return {"result": {'up': bitrate[0], 'down': bitrate[1]}}

    def get_current_bandwidth(self) -> Dict[str, str]:
        bitrate = self.fritz.get_current_bandwidth()
        return {"result": {'up': bitrate[0], 'down': bitrate[1]}}

    def fritz_info(self) -> Dict[str, str]:
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
