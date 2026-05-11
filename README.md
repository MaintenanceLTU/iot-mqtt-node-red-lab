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
- Application: `ltu1X`

---

## Step 2: Python Sensor (on your computer)

We use psutil to read sensor data from your computer. You can explore available monitoring functions here:
https://psutil.readthedocs.io/

### Install dependency
```bash
pip install paho-mqtt psutil
```

### Example script
```python
import paho.mqtt.client as mqtt
import time
import json
import psutil

BROKER = "YOUR_VM_PUBLIC_IP"
PORT = 1883
USERNAME = "myuser"
PASSWORD = "yourpass"
TOPIC = "D0022B/ltuXX"


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

## Step 3: Node-RED (Code Engine)

A Node-RED instance has already been prepared for you on IBM Cloud. 
- Browse to your Node-RED instance https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/red/. Replace XX with your app number. 
- Login with the same username and password that you used for the MQTT broker. After you have logged in, the Node-RED editor appears. 

### 1. Add MQTT-in node
- Drag **mqtt in** node
- Double-click → configure

### 2. Configure broker
- Server: `YOUR_VM_PUBLIC_IP`
- Port: `1883`
- Username: `myuser`
- Password: `yourpass`

### 3. Set topic
```
D0022B/ltuXX
```

---

## Step 4: Process data

### Add nodes:

```
mqtt in → json → function → chart
```

### Function node:
For example selecting cpu percentage value
```javascript
msg.payload = msg.payload.d.cpu.percent.value;
return msg;
```

---

## Step 5: Dashboard

Add:
- **Chart node** (line graph)
- **Gauge node** (optional)

Deploy and open dashboard URL https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/dashboard/.

---

## Step 6: Test

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
