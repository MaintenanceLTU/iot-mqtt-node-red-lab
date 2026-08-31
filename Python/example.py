# -*- coding: utf-8 -*-
import os
import time
import json
import psutil
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
BROKER = os.getenv("MQTT_BROKER")
PORT = 1883
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

CLIENT_ID = "ltuXX-deviceType-number" # e.g. ltu10-laptop-1
TOPIC = "coursecode/ltuXX/category" #e.g. D0022B/ltu10/data

# --- MQTT Callbacks for Status Logging ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"Successfully connected to MQTT broker at {BROKER}:{PORT}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    print("Disconnected from MQTT broker.")
    
# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

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
client.connect(BROKER, PORT, 60)
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
    
        # print(f"Published to [{TOPIC}]: {payload}")  # uncomment for debugging
    
        time.sleep(1)
       
except KeyboardInterrupt:
    print("\nScript stopped by user.")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    client.loop_stop()
    client.disconnect()