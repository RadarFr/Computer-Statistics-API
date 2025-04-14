from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import humanize
import os
import time
import psutil
import pynvml

os_name = os.system()
amd_intilized = False

if os_name == "Linux":
    import amdsmi
    from amdsmi import *
    print("You are running Linux, added AMD support has been initialized")
    amd_intilized = True

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
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

ifHasNvidaGPU = True # defaults to NVIDA GPU
ifHasAMDGPU = False

try:
    import pynvml
    pynvml.nvmlInit
except Exception:
    ifHasNvidaGPU = False

if amd_intilized == True:
    try:
        if ifHasNvidaGPU == False:
            amdsmi.init()
            ifHasAMDGPU = True
        else:
            pass
    except Exception:
        ifHasAMDGPU = False

@app.get("/stats")
def send_stats():
    response = {
        "SYSTEM":{
            "os_name": os.getlogin(),
            "os_system": os.system(),
            "os_version": os.version(),
        },
        "CPU": {
            "frequency": round(psutil.cpu_freq().current / 1000, 1),
            "utilization": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
            "temp":"Not Available",
        },
        "MEMORY": {
            "utilization": psutil.virtual_memory().percent,
            "total": humanize.naturalsize(psutil.virtual_memory().total, binary=True),
            "free": humanize.naturalsize(psutil.virtual_memory().free, binary=True),
            "used": humanize.naturalsize(psutil.virtual_memory().used, binary=True),
        },
        "DISK": {
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

    if ifHasAMDGPU and amd_intilized:
        try:
            devices = amdsmi.amdsmi_get_processor_handles()
            if len(devices) == 0:
                response["GPU"] = "No GPU available"
            else:
                for device in devices:
                    vram_usage = amdsmi.amdsmi_get_gpu_vram_usage(device)
                    response["GPU"] = {
                        "gpu_status": ifHasAMDGPU,
                        "name": ,
                        "temperature": ,
                        "utilization": ,
                        "mem_free": vram_usage[""],
                        "mem_used": vram_usage["vram_used"],
                        "mem_total": vram_usage["vram_total"],
                        "power_usage": ,
                    }
        except Exception as e:
            response["GPU"] = {"error": str(e)}
        
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
