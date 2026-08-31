# IoT Exercise using Arduino

## Objective
Read motion data from the Arduino Uno WiFi Rev2's built-in IMU, publish it to an MQTT broker, and visualise it in a Node-RED dashboard.

**Arduino sensor → MQTT broker → Node-RED → dashboard**

## Hardware and software

- Arduino Uno WiFi Rev2 and USB cable
- Arduino IDE
- Access to the course MQTT broker and Node-RED instance

Install these Arduino libraries using **Tools → Manage Libraries**:

- **WiFiNINA**
- **ArduinoMqttClient**
- **Arduino_LSM6DS3**

> The Uno WiFi Rev2 uses `WiFiNINA`. Do not use ESP8266, ESP32, or `WiFiS3` libraries.

## 1. Get the broker details

Use the values supplied by your teacher:

| Setting | Value |
|---|---|
| Broker | `YOUR_VM_PUBLIC_IP` |
| Port | `1883` |
| MQTT username | `myuser` |
| MQTT password | `yourpass` |
| MQTT topic | `coursecode/ltuXX`, e.g. `D0022B/ltu11` |

## 2. Upload the Arduino sketch

1. Open `uno_wifi_rev2_mqtt/uno_wifi_rev2_mqtt.ino` in the Arduino IDE.
2. Copy `arduino_secrets.h.example` to a new file named `arduino_secrets.h` in the same sketch folder.
3. Enter your Wi-Fi name and password in `arduino_secrets.h`.
4. In the sketch, set `broker`, `topic`, `username`, and `password` to the course values.
5. Select **Tools → Board → Arduino Uno WiFi Rev2** and its serial port.
6. Upload the sketch and open Serial Monitor at **9600 baud**.

The board publishes JSON every second. It contains the built-in IMU acceleration in g:

```json
{
  "ts": 12563,
  "d": {
    "acceleration": {
      "x": { "value": 0.014, "unit": "g" },
      "y": { "value": -0.025, "unit": "g" },
      "z": { "value": 0.996, "unit": "g" }
    }
  }
}
```

`ts` is device uptime in milliseconds, not calendar time. Node-RED supplies the dashboard timestamp.


## 4. Test

1. Power the Arduino and verify that Serial Monitor reports Wi-Fi and MQTT connections.
2. Deploy the Node-RED flow.
3. Open the dashboard page.
4. Move or tilt the board; the displayed acceleration should change.

## Troubleshooting

- **`WiFiNINA module not found`:** confirm that the selected board is *Arduino Uno WiFi Rev2*.
- **Wi-Fi does not connect:** check `arduino_secrets.h`; use a 2.4 GHz network.
- **MQTT error:** recheck broker address, credentials, and topic. Port `1883` is unencrypted MQTT.
- **No values on dashboard:** make sure the MQTT-in topic exactly matches the sketch topic and deploy the flow again.

## Optional extensions

- Publish all three acceleration axes to separate dashboard series.
- Add a vibration alert when the absolute acceleration departs from its normal range.
- Replace the uptime timestamp with NTP-synchronised epoch time.
