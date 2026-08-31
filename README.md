# IoT Exercise: Sensor → MQTT → Dashboard

## Objective
Develop basic IoT skills by creating, transmitting, and visualizing sensor data, and understand how such architectures are used for condition monitoring.

## MQTT naming

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


## Tutorials
Choose the tutorial that matches your sensor platform.

- [Arduino Uno WiFi Rev2](Arduino/tutorial_arduino_uno_wifi_rev2.md)  
  Read accelerometer data from the built-in IMU and publish it to MQTT.

- [Python](Python/tutorial_python.md)  
  Read CPU and battery data from your computer and publish it to MQTT.

Both tutorials use the same MQTT broker and Node-RED dashboard ([Node-RED tutorial](NodeRed/tutorial_nodered.md)).