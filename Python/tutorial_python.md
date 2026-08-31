# IoT Exercise using Python
Read sensor data from your local computer, publish it to an MQTT broker, and visualise it in a Node-RED dashboard.

**Sensor (your computer) → MQTT broker → Node-RED dashboard**

## Prerequisites: Python
You need Python installed on your computer to run the sensor script.

### Install Python
Download and install Python from:
https://www.python.org/downloads/

During installation, check **"Add Python to PATH"**.

You can run the scripts using:
- Command Prompt / Terminal, or
- Visual Studio Code (optional): https://code.visualstudio.com/docs/languages/python

#### Alternatives

There are also other Python distributions, e.g. Anaconda:
https://www.anaconda.com

The full Anaconda distribution is not necessary. Instead, you can install the lightweight version Miniconda:
https://www.anaconda.com/docs/getting-started/miniconda/main

A Python IDE included in Anaconda is Spyder, which can be installed using the Anaconda prompt:
`conda install spyder`

---
## Data Flow

```
Laptop sensors (Python)
        ↓
MQTT Broker (Mosquitto on IBM VM)
        ↓
Node-RED application (IBM cloud engine)
        ↓
Dashboard (web browser)
```

---

## Step 1: MQTT Broker

Your teacher provides:
- Broker IP: `YOUR_VM_PUBLIC_IP` #e.g. "156.xxx.xxx.xxx"
- Port: `1883`
- Username: `myuser` #e.g. ltu10
- Password: `yourpass`
- Application ID: `ltuXX`

Use 
 - Client id: `application_id-deviceType-number` # e.g. ltu10-laptop-1
 - Topic: `course_code/application_id/data` #e.g. D0022B/ltu10/data

---

## Step 2: Python Sensor (on your computer)

We use psutil to read sensor data from your computer. You can explore available monitoring functions here:
https://psutil.readthedocs.io/

### Install dependency
```bash
pip install paho-mqtt psutil
```

### Example script
See also [example.py](example.py)
```python
import paho.mqtt.client as mqtt
import time
import json
import psutil

BROKER = "YOUR_VM_PUBLIC_IP" 
PORT = 1883
CLIENT_ID = "ltuXX-deviceType-number" 
USERNAME = "ltuXX" 
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
```

---

## Step 3: Node-RED
A Node-RED app has already been prepared for you on IBM Cloud. Please follow these [instructions](../NodeRed/tutorial_nodered.md)


## Test

1. Run Python script
2. Open Node-RED dashboard
3. You should see live updates

---

## Optional Extensions

- Add multiple sensors (CPU, battery, etc.)
- Sync timestamp using NTP client 
- Add alerts (e.g. if value > threshold)

---

### Example using NTP client
Timestamps is important in IoT application. NTP time server client will be used to receive exact timestamp to your device. You can find more information about NTP here:
https://en.wikipedia.org/wiki/Network_Time_Protocol.

#### Install dependency
```bash
pip install ntplib
```

#### Use provided helpers.py and import the TimeClient
For code see [helpers.py](helpers.py)
```python
from helpers import NTPTimeClient
```
#### Before the main while loop, initialise the time client and sync it
```python
time_client = NTPTimeClient()
time_client.sync_ntp()
```
#### Replace the timestamp (ts) with the synced timeClient
```python
ts = time_client.get_epoch_time("ms")
```
