import os
from typing import Dict, Optional, Tuple
from fastapi import Request, FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from websockets import ConnectionClosedOK
from datetime import datetime
from configparser import ConfigParser
from util.auth import JWTValidator
from util.service import Service
import uvicorn
import multiprocessing

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

service = Service(config)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["BACKEND"]["ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_validator = JWTValidator(config=config["AUTH0"])


@app.get("/ping")
def ping() -> str:
    return datetime.now().isoformat()


@app.get("/idle")
def idle(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.idle()


@app.get("/uptime")
# returns uptime in in seconds
def uptime(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.uptime()


@app.websocket("/usage")
async def system_stats(websocket: WebSocket,
                       rate: Optional[int] = 1,
                       jwt=Depends(
                           jwt_validator.verify(permission='guest',
                                                query=True))):
    return await service.server_stats(websocket, rate)


@app.websocket("/net")
async def net_stats(websocket: WebSocket,
                    rate: Optional[int] = 1,
                    jwt=Depends(
                        jwt_validator.verify(permission='guest', query=True))):
    return await service.net_stats(websocket, rate)


@app.get("/shutdown")
def shutdown(jwt=Depends(jwt_validator.verify(permission='admin'))):
    return service.shutdown()


@app.get("/reboot")
def reboot(jwt=Depends(jwt_validator.verify(permission='admin'))):
    return service.reboot()


@app.get("/vm/all")
def all_vms(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.all_vms()


@app.get("/vm/active")
def active_vms(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.active_vms()


@app.put("/vm/{domain}")
async def edit_vm(domain,
                  request: Request,
                  jwt=Depends(jwt_validator.verify(permission='admin'))):
    return await service.edit_vm(domain, request)


@app.get("/vm/{domain}/info")
def vm_info(domain, jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.vm_info(domain)


@app.post("/vm/{domain}/start")
def start_vm(domain: str,
             jwt=Depends(jwt_validator.verify(permission='admin'))):
    return service.start_vm(domain)


@app.post("/vm/{domain}/stop")
def stop_vm(domain: str,
            jwt=Depends(jwt_validator.verify(permission='admin'))):
    return service.stop_vm(domain)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run("main:app",
                host=config["BACKEND"]["HOST"],
                port=int(config["BACKEND"]["PORT"]),
                reload=True)
