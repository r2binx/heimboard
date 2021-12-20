import subprocess
from util.auth import JWTValidator
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from configparser import ConfigParser
import os

app = FastAPI()

env = os.getenv("ENV", ".config")
config = []
if env == ".config":
    config = ConfigParser()
    config.read(".config")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["BACKEND"]["ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_validator = JWTValidator(config=config["AUTH0"])


@app.get("/ping")
def ping():
    dt_now = datetime.now().isoformat()
    print(dt_now)
    return dt_now


@app.get("/wakeup")
def wake(jwt=Depends(jwt_validator.verify(permission='guest'))):
    cmd = subprocess.check_output("wakeonlan " + config["BACKEND"]["WOL_MAC"],
                                  shell=True).strip()
    return cmd
