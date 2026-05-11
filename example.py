# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import json
import psutil

BROKER = "YOUR_VM_PUBLIC_IP"
PORT = 1883
USERNAME = "myuser"
PASSWORD = "yourpass"
TOPIC = "D0022B/ltu1X"


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)
client.loop_start()
        

def read_data():
    data = {}
    
    # Read cpu percentage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    data["cpu"] = {
        "percent" : {
            "value": cpu_percent
            }
        }
    
    # Read battery performance
    batt = psutil.sensors_battery()  
    if batt:
        data["battery"] = {
            "percent": { 
                "value": batt.percent
                },
            "plugged": { 
                "value": batt.power_plugged
                }
        }
    
    return data

# --- Start ---
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
    client.disconnect()