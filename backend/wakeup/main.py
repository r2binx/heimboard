import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    dt_now = datetime.now().isoformat()
    print(dt_now)
    return dt_now


@app.get("/wakeup")
def wake():
    cmd = subprocess.check_output("wakeonlan 00:1D:A5:1B:1C:1D",
                                  shell=True).strip()
    return cmd