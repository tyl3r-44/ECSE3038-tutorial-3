from pickle import GET

from fastapi import FastAPI, HTTPException

app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]
def average_temp(devices):
    total = sum(device['temp'] for device in devices)
    return total / len(devices) if devices else 0

print(f"Average Temperature: {average_temp(readings)}")
average_temp(readings)

def hottest(devices):
    return max(devices, key=lambda device: device['temp'])

print(f"Hottest Device: {hottest(readings)['name']}, Temperature: {hottest(readings)['temp']}")
hottest(readings)

@app.get("/devices")
def get_devices():
    return readings

@app.get("/devices/hottest")
def get_hottest_device():
    return hottest(readings)

@app.get("/devices/online")
def get_online_devices():
    return [device for device in readings if device['online']]

@app.get("/devices/{name}")
def get_device_by_name(name: str):
    device = next((d for d in readings if d['name'] == name), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.get("/stats")
def get_stats():
    return {
        "total_devices": len(readings),
        "online_devices": len([device for device in readings if device['online']]),
        "average_temperature": average_temp(readings),
        "hottest_device": hottest(readings)
    }
@app.post("/devices")
def add_device(device: dict):   
    return device

@app.get("/rooms/{room}/devices")
def get_devices_by_room(room: str):
    return [device for device in readings if device['room'] == room]