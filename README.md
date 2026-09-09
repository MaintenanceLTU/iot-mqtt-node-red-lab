# IoT Tutorial: Sensor → MQTT → Dashboard

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

- [Python (PC/Laptop)](Python/tutorial_python.md)  
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
Sensor data is sent as a JSON message with a timestamp (`ts`) and measurements (`d`), using the following structure:

```json
{
  "ts": 1710000000000,
  "d": {
    "metric_name": {
      "value_name": {
        "value": 1.0,
        "unit": "unit_string"
      }
    }
  }
}
```
#### Field Specifications

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `ts` | Integer | Yes | UNIX epoch timestamp in milliseconds (e.g., `1710000000000`). |
| `d` | Object | Yes | Data container containing all measurement data. |
| `d.<metric>` | Object | Yes | Grouping object for a sensor or telemetry group (e.g., `acceleration`, `cpu`). |
| `d.<metric>.<key>.value` | Number / Bool | Yes | Numerical or boolean reading value. |
| `d.<metric>.<key>.unit` | String | No | Unit of measurement (e.g., `"g"`, `"%"`). |

#### Example Payload
```json
{
  "ts": 1710000000000,
  "d": {
    "acceleration": {
        "x": {
            "value": 1.0,
            "unit": "g"
        }
    }
  }
}
```


#### JSON Schema
```json
{
  "$schema": "[https://json-schema.org/draft/2020-12/schema](https://json-schema.org/draft/2020-12/schema)",
  "title": "SensorDataPayload",
  "type": "object",
  "required": ["ts", "d"],
  "properties": {
    "ts": {
      "type": "integer",
      "description": "UNIX epoch timestamp in milliseconds"
    },
    "d": {
      "type": "object",
      "description": "Container for all sensor measurement readings",
      "additionalProperties": {
        "type": "object",
        "description": "Sensor metric or grouping (e.g. acceleration)"
      }
    }
  }
}
```

## License

Unless otherwise stated:
* Source code is licensed under the [MIT License](LICENSE-CODE).
* Original non-code content is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE-CONTENT.md).
