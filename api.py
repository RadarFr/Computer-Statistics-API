from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import clr
import humanize
import os
import pynvml
import math
import psutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
pynvml.nvmlInit()

@app.get("/stats")
def send_stats():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return {
        "win_username": os.getlogin(),
        "status": "Online",
        "CPU": {
            "frequency": round(psutil.cpu_freq().current/1000,1),
            "utilization": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
        },
        "Memory": { 
            "utilization": psutil.virtual_memory().percent,
            "total": humanize.naturalsize(psutil.virtual_memory().total, binary=True),
            "free": humanize.naturalsize(psutil.virtual_memory().free, binary=True),
            "used": humanize.naturalsize(psutil.virtual_memory().used, binary=True),
        },
        "Disk": {
            "utilization": humanize.naturalsize(psutil.disk_usage("C:").used),
            "free": humanize.naturalsize(psutil.disk_usage("C:").free),
            "total": humanize.naturalsize(psutil.disk_usage("C:").total),
            "percent": psutil.disk_usage("C:").percent,
        },
        "GPU": {
            "name": pynvml.nvmlDeviceGetName(handle),
            "temperature": pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU), 
            "utilization": pynvml.nvmlDeviceGetUtilizationRates(handle).gpu,
            "mem_free": humanize.naturalsize(memory_info.free, binary=True),
            "mem_used": humanize.naturalsize(memory_info.used, binary=True),
            "mem_total": humanize.naturalsize(memory_info.total, binary=True),
            "power_usage": str(round(pynvml.nvmlDeviceGetPowerUsage(handle) / 1000)) + " W"
        }
    }

# uvicorn api:app --host 0.0.0.0 --port 8000 --reload
