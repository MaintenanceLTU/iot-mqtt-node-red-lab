# IoT Exercise: Sensor → MQTT → Dashboard

## Objective
Develop basic IoT skills by creating, transmitting, and visualizing sensor data, and understand how such architectures are used for condition monitoring.

**Sensor (your computer) → MQTT broker → Node-RED dashboard**

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
- Broker IP: `YOUR_VM_PUBLIC_IP`
- Port: `1883`
- Username: `myuser`
- Password: `yourpass`
- Application: `ltuXX`

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
USERNAME = "myuser"
PASSWORD = "yourpass"
TOPIC = "coursecode/ltuXX" #e.g. D0022B/ltu11


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)
client.loop_start()
        

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
```

---

## Step 3: Node-RED

A Node-RED app has already been prepared for you on IBM Cloud. 
- Browse to your Node-RED instance https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/. Replace XX with your app number. 
- Login with the same username and password that you used for the MQTT broker. After you have logged in, the Node-RED editor appears. 

#### Build flow to process data
```
mqtt in → function → dashboard (e.g. chart or gauge)
```

### 3.1 Add MQTT-in node
- Drag **mqtt in** node
- Double-click → configure
    - Server: `YOUR_VM_PUBLIC_IP`
    - Port: `1883`
    - Username: `myuser`
    - Password: `yourpass`
- Set topic `coursecode/ltuXX`, e.g. `D0002B/ltu11`. The topic needs to match the topic in your Python code.

### 3.2 Add function node
- Drag **function** node 
- Example selecting cpu percentage value
```javascript
const ts = msg.payload.ts;
const data = msg.payload.d;
msg.timestamp = ts;
msg.payload = data.cpu.percent.value;
return msg;
```

### 3.3 Add dashboard node
- Install palette @flowfuse/node-red-dashboard
    - In the menu select Manage palette
    - In the Install tab, search for @flowfuse/node-red-dashboard
    - Press install (can take some minutes)
- Drag selected node, e.g.:
    - **Chart node** (line graph)
    - **Gauge node** 
- Double-click → configure
    - Create or modify Dashboard Group and Page


## Step 4: Deploy
Deploy and open dashboard URL https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/dashboard/.
- Replace XX with your appnumber
- Use the subdomain specified in the dahsboard page configureation, default is dashboard

### Test

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
from helpers import TimeClient
```
#### Before the main while loop, initialise the time client and sync it
```python
timeClient = TimeClient()
timeClient.syncTime()
```
#### Replace the timestamp (ts) with the synced timeClient
```python
ts = timeClient.getEpochTime("ms")
```
