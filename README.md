# IoT Exercise: Sensor → MQTT → Dashboard

## Objective
Develop basic IoT skills by creating, transmitting, and visualizing sensor data, and understand how such architectures are used for condition monitoring.

## Introduction
Architecture & Data Flow
```text
[ Sensor / Publisher ] ---> ( MQTT Broker: Mosquitto ) ---> [ Node-RED Subscriber / Dashboard ]
```
An MQTT broker receives messages from publishers and routes them to subscribers based on matching topics. In this exercise, we use Mosquitto, an open-source lightweight message broker that implements the MQTT protocol.
- [MQTT introduction](https://mqtt.org/)
- [Eclipse Mosquitto](https://mosquitto.org/)

Node-RED is a low-code tool for building event-driven applications. In this exercise, it receives MQTT messages, processes the sensor data, and displays it on a dashboard.
- [Node-RED documentation](https://nodered.org/docs/)
- [Node-RED tutorials](https://nodered.org/docs/tutorials/)

## Tutorials
Choose the tutorial that matches your sensor platform.

- [Arduino Uno WiFi Rev2](Arduino/tutorial_arduino_uno_wifi_rev2.md)  
  Read accelerometer data from the built-in IMU and publish it to MQTT.

- [Python](Python/tutorial_python.md)  
  Read CPU and battery data from your computer and publish it to MQTT.

Both tutorials use the same MQTT broker and Node-RED dashboard. Once your sensor code is sending data, follow the [Node-RED tutorial](NodeRed/tutorial_nodered.md) to set up your dashboard (this link is also included in each platform tutorial).

## MQTT Identifiers and Topics

### Client ID

Use this format:

`application-deviceType-number`

Examples:

- `ltu10-laptop-1`
- `ltu10-rpi-1`
- `ltu10-arduino-2`

### Topic

Topics are usually organized as:

`organization/device/category`

In this exercise:

- organization = course code
- device = application ID
- category = message type

Use `data` for sensor measurements, for example:

`D0023B/ltu10/data`

| Category | Meaning |
|---|---|
| `data` / `telemetry` | Sensor measurements |
| `status` | Online/offline or device state |
| `event` | Events |
| `alert` | Alarms or warnings |
| `command` | Commands sent to device |
| `config` | Configuration data |

### Message Format
Sensor data is sent as a JSON message with a timestamp (`ts`) and measurements (`d`). 

```json
{
  "ts": 1710000000000,
  "d": {
    "sensor": {
      "value": 1.0,
      "unit": "unit"
    }
  }
}
```
`ts` is a Unix epoch timestamp in milliseconds.

