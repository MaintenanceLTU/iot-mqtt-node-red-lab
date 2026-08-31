# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import json
import psutil

BROKER = "YOUR_VM_PUBLIC_IP" #e.g. "156.xxx.xxx.xxx"
PORT = 1883
CLIENT_ID = "ltuXX-deviceType-number" # e.g. ltu10-laptop-1
USERNAME = "ltuXX" #e.g. ltu10
PASSWORD = "yourpass" #In production systems, credentials should not be hardcoded in source code.
TOPIC = "coursecode/ltuXX/category" #e.g. D0022B/ltu10/data

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)
        

def read_data():
    data = {}
    
    # Read CPU percentage
    # interval=None → non-blocking, returns usage since last call (first call returns 0.0)
    # interval=1 → blocks for 1 s and returns average CPU usage over that period
    # Use interval=None for continuous loops, or a small value (e.g. 0.1) for sampling
    cpu_percent = psutil.cpu_percent(interval=None)
    data["cpu"] = {
        "percent" : {
            "value": cpu_percent,
            "unit": "%"
            }
        }
    
    # Read battery performance
    batt = psutil.sensors_battery()  
    if batt:
        data["battery"] = {
            "percent": { 
                "value": batt.percent,
                "unit": "%"
                },
            "plugged": { 
                "value": batt.power_plugged
                }
        }
    
    return data

# --- Start ---
client.loop_start()
try:
        
    while True:
        ts = int(time.time()*1e3) #epoch time in ms
        
        data = read_data()
    
        payload = {
            'ts': ts,
            'd': data
        }
    
        client.publish(TOPIC, json.dumps(payload))
    
        # print(payload)  # uncomment for debugging
    
        time.sleep(1)
        
except Exception as e:
    print(e)
finally:
    client.loop_stop()
    client.disconnect()