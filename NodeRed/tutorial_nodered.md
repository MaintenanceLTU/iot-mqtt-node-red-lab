# Node-RED
A Node-RED app has already been prepared for you on IBM Cloud. 
- Browse to your Node-RED instance https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/. Replace XX with your app number. 
- Login with the your provided user and password (same as for the MQTT broker). 
- After you have logged in, the Node-RED editor appears. 

### Build flow to process data
```
mqtt in → function → dashboard (e.g. chart or gauge)
```

## 1 Add MQTT-in node

- Drag **mqtt in** node
- Double-click → configure
    - Server: `YOUR_VM_PUBLIC_IP`
    - Port: `1883`
    - Username: `myuser`
    - Password: `yourpass`
    - Client-ID: Leave empty or use an application identifier, e.g. `ltuXX-nodered`. Do **not** use the same Client-ID as for the sensor.

- Set topic `coursecode/ltuXX/category`, e.g. `D0023B/ltu10/data`. The topic needs to match the topic in your sensor code.
    - Use `coursecode/ltuXX/+`, e.g. `D0023B/ltu10/+`, to subscribe to all categories.

## 2 Add function node
- Drag **function** node 

### Example Ardunio: Selecting z-axis acceleration
Select the z-axis acceleration (normally about `1 g` when the board lies flat):

```javascript
const ts = msg.payload.ts;
const data = msg.payload.d;
msg.timestamp = ts;
msg.payload = data.acceleration.z.value;
return msg;
```

### Example Python: Selecting cpu percentage value
```javascript
const ts = msg.payload.ts;
const data = msg.payload.d;
msg.timestamp = ts;
msg.payload = data.cpu.percent.value;
return msg;
```

## 3 Add dashboard node
- Install the dashboard nodes:
    - Open the menu (top right) → **Manage palette**
    - Go to the **Install** tab
    - Search for `@flowfuse/node-red-dashboard`
    - Click **Install** (this may take a minute and Node-RED may restart)

- After installation, new nodes appear in the palette:
    - Drag a **Chart** node (time series), or
    - Drag a **Gauge** node (current value)

- Double-click the selected dashboard node → configure:
    - Create or select a **Dashboard group**
    - Assign the group to a **Dashboard page**
    - Configure label, units, and display options


## 4 Deploy
Deploy and open dashboard URL https://ltuXX.16qp5wjqoncr.eu-de.codeengine.appdomain.cloud/dashboard/.
- Replace XX with your appnumber
- Use the subdomain specified in the dahsboard page configureation, default is dashboard