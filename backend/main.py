import ast
import multiprocessing
import os
import sys
from configparser import ConfigParser
from datetime import datetime
from typing import Optional, Dict, Union

import uvicorn
from fastapi import Request, FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware

import src.util.service as services
from src.util.auth import JWTValidator

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

service = services.Service(config)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ast.literal_eval(config["BACKEND"]["ORIGINS"])),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_validator = JWTValidator(config=config["AUTH0"])


@app.get("/ping")
def ping() -> str:
    return datetime.now().isoformat()


@app.get("/active")
def idle(jwt=Depends(jwt_validator.verify(permission='guest'))) -> Dict[str, Union[bool, str, Dict]]:
    return service.active_services()


@app.get("/uptime")
# returns uptime in in seconds
def uptime(jwt=Depends(jwt_validator.verify(permission='guest'))) -> int:
    return services.uptime()


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


@app.get("/fritz/info")
def fritz_info(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.fritz_info()


@app.get("/shutdown")
def shutdown(jwt=Depends(jwt_validator.verify(permission='admin'))):
    return services.shutdown()


@app.get("/reboot")
def reboot(jwt=Depends(jwt_validator.verify(permission='admin'))):
    return services.reboot()


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


@app.get("/storage/usage")
def storage_usage(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return service.storage_usage()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    reload = True if len(sys.argv) > 1 and sys.argv[1] == "reload" else False
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=int(config["BACKEND"]["PORT"]),
                reload=reload)
