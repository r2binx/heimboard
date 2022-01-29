import ast
import asyncio
import json
import multiprocessing
import os
import sys
import subprocess
from configparser import ConfigParser
from datetime import datetime
from typing import Union, Dict

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from util.auth import JWTValidator

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

server_ip = config["WAKEUP"]["BACKEND_IP"]
server_mac = config["WAKEUP"]["WOL_MAC"]


def get_schedule() -> Dict[str, Union[str, int]]:
    if os.path.exists("schedule.json"):
        with open("schedule.json", "r") as f:
            sched = json.load(f.read())
            # convert to millis
            sched["time"] = sched["time"] * 1000
            return sched
    else:
        schedule = {"time": "", "action": "boot"}
        with open("schedule.json", "w") as f:
            f.write(json.dumps(schedule))

        return schedule


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ast.literal_eval(config["BACKEND"]["ORIGINS"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_validator = JWTValidator(config=config["AUTH0"])


def wol(mac):
    print(f"Waking up {mac}")
    cmd = subprocess.check_output(["wakeonlan", mac]).strip()
    return cmd


class ScheduledTime(BaseModel):
    time: Union[int, None]
    action: str


class ScheduleService:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    task: asyncio.Task

    def __init__(self):
        self.task = self.loop.create_task(self.run_schedule())

    def ping(self, ip):
        try:
            subprocess.check_output(["ping", "-c", "1", ip])
            return True
        except subprocess.CalledProcessError:
            return False

    async def run_schedule(self):
        while True:
            curr_schedule = get_schedule().get("time")
            if curr_schedule is not None and curr_schedule != "":
                ts = datetime.fromtimestamp(int(curr_schedule))
                now = datetime.now()
                scheduled_boot = now.replace(hour=ts.hour, minute=ts.minute)

                # if the scheduled time is in the past, check if the server is up
                # else boot the server
                if scheduled_boot.time() < now.time():
                    online = self.ping(server_ip)
                    if not online:
                        wol(server_mac)
                        # give it some time to boot
                        await asyncio.sleep(120)

            await asyncio.sleep(60)


schedule_service = ScheduleService()


@app.get("/ping")
def ping():
    return datetime.now().isoformat()


@app.get("/wakeup")
def wake(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return wol(server_mac)


@app.post("/boot-schedule")
def schedule_boot(data: ScheduledTime, jwt=Depends(jwt_validator.verify(permission='admin'))):
    if data.time is None:
        new_schedule = {"time": 0, "action": "boot"}
        with open("schedule.json", "w") as f:
            f.write(json.dumps(new_schedule))
    else:
        ts = datetime.fromtimestamp(data.time / 1e3)

        new_schedule = {"time": {int(ts.timestamp() * 1000)}, "action": "boot"}
        with open("schedule.json", "w") as f:
            f.write(json.dumps(new_schedule))


@app.get("/boot-schedule")
def get_boot_schedule(jwt=Depends(jwt_validator.verify(permission='guest'))):
    return get_schedule()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    reload = True if len(sys.argv) > 1 and sys.argv[1] == "reload" else False
    uvicorn.run("wakeup:app",
                host="0.0.0.0",
                port=int(config["WAKEUP"]["WAKEUP_PORT"]),
                reload=reload)
