# IoT Exercise using Arduino

## Objective
Read motion data from the Arduino Uno WiFi Rev2's built-in IMU, publish it to an MQTT broker, and visualise it in a Node-RED dashboard.

**Sensor (Arduino Uno WiFi Rev2) → MQTT broker → Node-RED dashboard**

## Prerequisites: Arduino IDE
You need Arduino IDE installed on your computer to run the sensor sketch.

### Install Arduino IDE
Download and install Arduino IDE from:
https://www.arduino.cc/en/software

You can run the sketches using:
- Arduino IDE, or
- Visual Studio Code with PlatformIO (optional): https://platformio.org/install/ide?install=vscode

#### Alternatives

There are also other Arduino development environments, e.g. Arduino Cloud Editor:
https://app.arduino.cc

The Arduino Cloud Editor is not necessary. Instead, you can install the Arduino IDE on your computer:
https://www.arduino.cc/en/software

---
## Data Flow

```
Arduino Uno WiFi Rev2 sensors
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

Use 
 - Client id: `application_id-deviceType-number` # e.g. ltu10-arduino-1
 - Topic: `course_code/application_id/data` #e.g. D0023B/ltu10/data


---

## Step 2: Arduino Sensor (on your computer)

We use the built-in IMU on the Arduino Uno WiFi Rev2 to read acceleration data. You can explore the Arduino library here:
https://docs.arduino.cc/libraries/arduino_lsm6ds3/

### Install dependency
In Arduino IDE, open **Tools → Manage Libraries** and install:
- `WiFiNINA`
- `NTPClient`
- `ArduinoMqttClient`
- `ArduinoJson`
- `Arduino_LSM6DS3`

Create a file called `arduino_secrets.h` in the same folder as the sketch, change to your recivied ip and credentials for the wifi and mqtt broker:
```cpp
#define SECRET_SSID "YOUR_WIFI_NAME"
#define SECRET_PASS "YOUR_WIFI_PASSWORD"

#define SECRET_BROKER "YOUR_VM_PUBLIC_IP"
#define SECRET_MQTT_USERNAME "myuser" 
#define SECRET_MQTT_PASSWORD "yourpass"
```


### Example script
See also [uno_wifi_rev2_mqtt.ino](uno_wifi_rev2_mqtt.ino)

```cpp
#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoMqttClient.h>
#include <ArduinoJson.h>
#include <Arduino_LSM6DS3.h>
#include "arduino_secrets.h"

char broker[] = SECRET_BROKER;
int port = 1883;
char username[] = SECRET_MQTT_USERNAME;
char password[] = SECRET_MQTT_PASSWORD;
char clientId[] = "ltuXX--2";
char topic[] = "coursecode/ltuXX/category";  // e.g. D0023B/ltu10/data

WiFiClient wifiClient;
MqttClient client(wifiClient);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

unsigned long epochAtSync = 0;
unsigned long millisAtSync = 0;

void connectWiFi() {
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to Wi-Fi...");
    WiFi.begin(SECRET_SSID, SECRET_PASS);
    delay(5000);
  }
  Serial.println("Wi-Fi connected.");
}

void syncTime() {
  while (!timeClient.forceUpdate()) {
    Serial.println("NTP synchronization failed. Retrying...");
    delay(5000);
  }
  epochAtSync = timeClient.getEpochTime();
  millisAtSync = millis();
}

uint64_t getEpochTimeMs() {
  return (uint64_t)epochAtSync * 1000ULL + (millis() - millisAtSync);
}

void connectMqtt() {
  client.setUsernamePassword(username, password);

  while (!client.connect(broker, port, clientId)) {
    Serial.print("MQTT connection failed, error code: ");
    Serial.println(client.connectError());
    delay(5000);
  }
  Serial.println("MQTT connected.");
}

void readData(JsonDocument &doc) {
  float x = 0.0;
  float y = 0.0;
  float z = 0.0;

  // Read acceleration in g
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
  }

  doc["d"]["acceleration"]["x"]["value"] = x;
  doc["d"]["acceleration"]["x"]["unit"] = "g";
  doc["d"]["acceleration"]["y"]["value"] = y;
  doc["d"]["acceleration"]["y"]["unit"] = "g";
  doc["d"]["acceleration"]["z"]["value"] = z;
  doc["d"]["acceleration"]["z"]["unit"] = "g";
}

void setup() {
  Serial.begin(9600);
  while (!Serial) { }

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("WiFiNINA module not found.");
    while (true) { }
  }
  if (!IMU.begin()) {
    Serial.println("IMU not detected.");
    while (true) { }
  }

  connectWiFi();
  timeClient.begin();
  syncTime();
  connectMqtt();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
    syncTime();
  }
  if (!client.connected()) connectMqtt();
  client.poll();

  DynamicJsonDocument doc(512);  // Bytes reserved for the JSON document
  char output[512];

  // Create JSON formatted data packet using ArduinoJson library
  doc["ts"] = getEpochTimeMs();
  readData(doc);

  serializeJson(doc, output);
  client.beginMessage(topic);
  client.print(output);
  client.endMessage();

  // serializeJson(doc, Serial);  // uncomment for debugging
  delay(1000);
}
```

---

## Step 3: Node-RED
A Node-RED app has already been prepared for you on IBM Cloud. Please follow these [instructions](../NodeRed/tutorial_nodered.md)


## Test

1. Upload the Arduino sketch.
2. Open the Node-RED dashboard.
3. You should see live updates.

---

## Optional Extensions

- Add multiple sensors (X, Y, Z acceleration, etc.)
- Add alerts (e.g. if value > threshold)

---