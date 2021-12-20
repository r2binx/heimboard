import os
import psutil
import asyncio
import subprocess
from typing import Optional, Tuple
from fastapi import Request, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from websockets import ConnectionClosedOK
from datetime import datetime
import time
from configparser import ConfigParser
from util.jelly import Jelly
from util.kvm import KVM
from util.plex import Plex
from util.sabnzbd import Sabnzbd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

kvm = KVM()
jelly = Jelly(config["JELLY"])
plex = Plex(config["PLEX"])
nzb = Sabnzbd(config["NZB"])


@app.get("/ping")
def ping():
    dt_now = datetime.now().isoformat()
    print(dt_now)
    return dt_now


@app.get("/idle")
def idle():
    idle_check = check_all_idle()
    idle = idle_check[0]
    details = idle_check[1]

    return {"result": idle, "idle": details}


@app.get("/uptime")
# returns uptime in in seconds
def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return round(uptime_seconds)


@app.websocket("/usage")
async def system_stats(websocket: WebSocket, rate: Optional[int] = 1):
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


def convert_to_mbit(value):
    return value / 1024. / 1024. / 1024. * 8


@app.get("/shutdown")
def shutdown():
    idle = check_all_idle()
    if idle[0]:
        cmd = subprocess.check_output('sudo shutdown', shell=True).strip()
        return {"success": True, "message": cmd}
    else:
        return {"success": False, "message": "System is not idle"}


@app.get("/reboot")
def reboot():
    idle = check_all_idle()
    if idle[0]:
        cmd = subprocess.check_output('sudo shutdown -r', shell=True).strip()
        return {"success": True, "message": cmd}
    else:
        return {"success": False, "message": "System is not idle"}


@app.get("/vm/all")
def all_vms():
    vms = kvm.get_vms()
    sorted_vms = sorted(vms, key=lambda d: d['name'])
    response = {"result": []}
    for vm in sorted_vms:
        response["result"].append(vm)

    return response


@app.get("/vm/active")
def active_vms():
    vms = kvm.get_active()
    response = {"result": []}
    for vm in vms:
        response["result"].append({
            "name": vm[0],
            "state": vm[1],
        })

    return response


@app.put("/vm/{domain}")
async def edit_vm(domain, request: Request):
    data = await request.json()
    for k, v in data.items():
        if k == "memory":
            result = kvm.set_active_memory(domain, v)

            return {"result": result.status}
        elif k == "state":
            if v == "start" or v == "boot":
                result = kvm.boot_vm(domain)
                return {"result": result.status}
            elif v == "stop" or v == "shutdown":
                result = kvm.shutdown_vm(domain)
                return {"result": result.status}
            elif v == "destroy":
                result = kvm.destroy_vm(domain)
                return {"result": result.status}

        else:
            return {
                "result": {
                    "success": False,
                    "message": f"'{k}' not implemented"
                }
            }


@app.get("/vm/{domain}/info")
def vm_info(domain):
    result = kvm.get_vm_info(domain)

    return {"result": result.status}


@app.post("/vm/{domain}/start")
def start_vm(domain: str):
    result = kvm.boot_vm(domain)

    return {"result": result.status}


@app.post("/vm/{domain}/stop")
def stop_vm(domain: str):
    result = kvm.shutdown_vm(domain)

    return {"result": result.status}


def check_all_idle() -> Tuple[bool, dict[str, bool]]:
    jelly_idle = jelly.is_jelly_idle()
    plex_idle = plex.is_plex_idle()
    kvm_idle = kvm.is_kvm_idle()
    nzb_idle = nzb.is_nzb_idle()

    return (jelly_idle and plex_idle and kvm_idle and nzb_idle), {
        "jelly": jelly_idle,
        "plex": plex_idle,
        "nzb": nzb_idle,
        "kvm": kvm_idle
    }
