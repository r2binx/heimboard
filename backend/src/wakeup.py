import ast
import json
import multiprocessing
import os
import subprocess
from configparser import ConfigParser
from datetime import datetime
from typing import Union

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from util.auth import JWTValidator


class ScheduledTime(BaseModel):
    schedule: Union[int, None]


app = FastAPI()

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ast.literal_eval(config["BACKEND"]["ORIGINS"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_validator = JWTValidator(config=config["AUTH0"])


@app.get("/ping")
def ping():
    return datetime.now().isoformat()


@app.get("/wakeup")
def wake(jwt=Depends(jwt_validator.verify(permission='guest'))):
    cmd = subprocess.check_output(["wakeonlan",
                                   config["BACKEND"]["WOL_MAC"]]).strip()
    return cmd


@app.post("/bootSchedule")
def schedule_boot(data: ScheduledTime, jwt=Depends(jwt_validator.verify(permission='admin'))):
    print(data)
    if data.schedule is None:
        with open("schedule.json", "w") as f:
            f.write(json.dumps({"time": "", "action": "boot"}))
    else:
        ts = datetime.fromtimestamp(data.schedule / 1e3)
        now = datetime.now()
        scheduled_boot = now.replace(hour=ts.hour, minute=ts.minute)

        with open("schedule.json", "w") as f:
            f.write(json.dumps({"time": f"{int(scheduled_boot.timestamp())}", "action": "boot"}))

        if scheduled_boot.time() < now.time():
            print("is after schedule:", scheduled_boot)
        else:
            print("is before schedule:", scheduled_boot)


@app.get("/bootSchedule")
def get_boot_schedule(jwt=Depends(jwt_validator.verify(permission='guest'))):
    if os.path.exists("schedule.json"):
        with open("schedule.json", "r") as f:
            schedule = json.loads(f.read())
            return schedule


if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run("wakeup:app", host="0.0.0.0", port=15050)
