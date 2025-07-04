from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import humanize
import os
import time
import psutil
import pynvml
import sys
import subprocess

cpu_name = subprocess.run(["powershell", "-Command", "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name"],capture_output=True, text=True).stdout.strip()
is_windows = hasattr(sys, 'getwindowsversion') 

if is_windows == False:
    import amdsmi
    from amdsmi import *

with open('games.json') as f:
    games = json.load(f)
    
def get_games():
    running_applications = []
    active_processes = set(proc.info['name']
                           for proc in psutil.process_iter(['pid', 'name']))

    for game in games:
        if game['exe'] in active_processes:
            print(f"{game['name']} is running")
            running_applications.append(game['name'])
    return str(running_applications)

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

ifHasNvidaGPU = True # defaults to NVIDA GPU
if is_windows == False:
    ifHasAMDGPU = False

try:
    import pynvml
    pynvml.nvmlInit
except Exception:
    ifHasNvidaGPU = False


if ifHasNvidaGPU == False and is_windows == False:
    try:
        if ifHasNvidaGPU == False:
            amdsmi.init()
            ifHasAMDGPU = True
        else:
            pass
    except Exception:
        ifHasAMDGPU = False

pynvml.nvmlInit()

@app.get("/stats")
def send_stats():
    response = {
        "win_username": os.getlogin(),
        "status": "Online",
        "CPU": {
            "frequency": round(psutil.cpu_freq().current / 1000, 1),
            "utilization": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
            "name":str(cpu_name)
        },
        "Memory": {
            "utilization": psutil.virtual_memory().percent,
            "total": humanize.naturalsize(psutil.virtual_memory().total, binary=True),
            "free": humanize.naturalsize(psutil.virtual_memory().free, binary=True),
            "used": humanize.naturalsize(psutil.virtual_memory().used, binary=True),
        },
        "Disk": {
            "utilization": humanize.naturalsize(psutil.disk_usage("C://").used),
            "free": humanize.naturalsize(psutil.disk_usage("C://").free),
            "total": humanize.naturalsize(psutil.disk_usage("C://").total),
            "percent": psutil.disk_usage("C://").percent,
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
    if is_windows == False:
        if ifHasAMDGPU:
            try:
                devices = amdsmi.amdsmi_get_processor_handles()
                if len(devices) == 0:
                    response["GPU"] = "No GPU available"
                else:
                    for device in devices:
                        vram_usage = amdsmi.amdsmi_get_gpu_vram_usage(device)
                        response["GPU"] = {
                            "gpu_status": ifHasAMDGPU,
                            #"name": ,
                            #"temperature": ,
                            #"utilization": ,
                            "mem_free": vram_usage[""],
                            "mem_used": vram_usage["vram_used"],
                            "mem_total": vram_usage["vram_total"],
                            #"power_usage": ,
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

@app.get("/applications")
def games_section():
    games = get_games()
    if games == "[]":
        games = "[No current Games]"
    return games
  
# Run with: uvicorn api:app --host 0.0.0.0 --port 8000 --reload
