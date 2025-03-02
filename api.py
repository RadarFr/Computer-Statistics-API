from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import humanize
import os
import time
import psutil
import pynvml

def getCoreUsage():

    time.sleep(1)
    
    cpu_usage_per_core = psutil.cpu_percent(percpu=True, interval=1)
    data = {
        "core": [],
        "usage": []
    }
    for i, usage in enumerate(cpu_usage_per_core):
        data["core"].append(i)
        data["usage"].append(usage)
    return data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

ifHasNvidaGPU = True
try:
    import pynvml
    pynvml.nvmlInit()
except Exception:
    ifHasNvidaGPU = False

@app.get("/stats")
def send_stats():
    response = {
        "win_username": os.getlogin(),
        "status": "Online",
        "CPU": {
            "frequency": round(psutil.cpu_freq().current / 1000, 1),
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
        }
    }

    if ifHasNvidaGPU:
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpu_name = pynvml.nvmlDeviceGetName(handle)

            response["GPU"] = {
                "gpu_status": ifHasNvidaGPU,
                "name": pynvml.nvmlDeviceGetName(handle),
                "temperature": pynvml.nvmlDeviceGetTemperature(handle,pynvml.NVML_TEMPERATURE_GPU),
                "utilization": pynvml.nvmlDeviceGetUtilizationRates(handle).gpu,
                "mem_free": humanize.naturalsize(memory_info.free, binary=True),
                "mem_used": humanize.naturalsize(memory_info.used, binary=True),
                "mem_total": humanize.naturalsize(memory_info.total, binary=True),
                "power_usage": f"{round(pynvml.nvmlDeviceGetPowerUsage(handle) / 1000)} W",
            }
        except Exception as e:
            response["GPU"] = {"error": str(e)}
    else:
        response["GPU"] = "No GPU available"



    return response

@app.get("/SlowerStats")
def send_SlowerStats():
    responce = {
        "status": "Online",
        "CPU": {
            "Cores":getCoreUsage()
       }
    }
    return responce
    

# Run with: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
