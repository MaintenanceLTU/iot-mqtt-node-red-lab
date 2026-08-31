# IoT Exercise using Arduino

## Objective
Read motion data from the Arduino Uno WiFi Rev2's built-in IMU, publish it to an MQTT broker, and visualise it in a Node-RED dashboard.

**Sensor (Arduino Uno WiFi Rev2) → MQTT broker → Node-RED dashboard**

## Prerequisites: Arduino IDE
You need Arduino IDE installed on your computer to run the sensor sketch.

### Install Arduino IDE
You can run the sketches using Arduino IDE. Download and install Arduino IDE from:
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

// --- MQTT & Broker Configurations ---
char broker[] = SECRET_BROKER;
int port = 1883;
char username[] = SECRET_MQTT_USERNAME;
char password[] = SECRET_MQTT_PASSWORD;
char clientId[] = "ltuXX-deviceType-number"; // e.g. ltu10-arduino-1
char topic[] = "coursecode/ltuXX/category";  // e.g. D0023B/ltu10/data

// --- Network & Protocol Objects ---
WiFiClient wifiClient;
MqttClient client(wifiClient);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// --- Time Synchronization Variables ---
unsigned long epochAtSync = 0;
unsigned long millisAtSync = 0;

void connectWiFi() {
  // Connects to the configured Wi-Fi network
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to Wi-Fi SSID: ");
    Serial.println(SECRET_SSID);
    WiFi.begin(SECRET_SSID, SECRET_PASS);
    delay(5000);
  }
  Serial.println("Wi-Fi connected.");
}

void syncTime() {
  // Synchronizes the internal clock with an NTP server
  while (!timeClient.forceUpdate()) {
    Serial.println("NTP synchronization failed. Retrying...");
    delay(5000);
  }
  epochAtSync = timeClient.getEpochTime();
  millisAtSync = millis();

  Serial.print("Time synchronized. Current UNIX epoch: ");
  Serial.println(epochAtSync);
}

uint64_t getEpochTimeMs() {
  // Calculates current timestamp in milliseconds using internal millis offset
  return (uint64_t)epochAtSync * 1000ULL + (millis() - millisAtSync);
}

void connectMqtt() {
  // Establishes connection to the MQTT broker using credentials
  client.setUsernamePassword(username, password);

  while (!client.connect(broker, port, clientId)) {
    Serial.print("MQTT connection failed, error code: ");
    Serial.println(client.connectError());
    Serial.println("Retrying MQTT connection ...");
    delay(5000);
  }
  Serial.println("MQTT connected.");
}

void readData(JsonDocument &doc) {
  // Reads IMU accelerometer values and builds the JSON structure

  // Initiates acceleration variables
  float x = 0.0;
  float y = 0.0;
  float z = 0.0;

  // Read acceleration in g
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
  }

  // Structure the payload according to the JSON schema
  doc["d"]["acceleration"]["x"]["value"] = x;
  doc["d"]["acceleration"]["x"]["unit"] = "g";
  doc["d"]["acceleration"]["y"]["value"] = y;
  doc["d"]["acceleration"]["y"]["unit"] = "g";
  doc["d"]["acceleration"]["z"]["value"] = z;
  doc["d"]["acceleration"]["z"]["unit"] = "g";
}

void setup() {
  // Use 115200 baud rate for faster data transfer to Serial Monitor
  Serial.begin(115200);
  while (!Serial) { }

  // Verify hardware initialization
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("WiFiNINA module not found.");
    while (true) { }
  }
  if (!IMU.begin()) {
    Serial.println("IMU not detected.");
    while (true) { }
  }

  // Initialize network and messaging protocols
  connectWiFi();
  timeClient.begin();
  syncTime();
  connectMqtt();

  Serial.println("--- Setup completed ---");
}

void loop() {
  // Re-establish Wi-Fi connection if lost
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi connection lost. Reconnecting...");
    connectWiFi();
    syncTime();
  }

  // Re-establish MQTT connection if lost
  if (!client.connected()) {
    Serial.println("MQTT connection lost. Reconnecting...");
    connectMqtt();
  }

  // Keep the MQTT client active
  client.poll();

  // Create JSON payload document (ArduinoJson v6)
  JsonDocument doc;
  
  // Populate the JSON payload with timestamp and data
  doc["ts"] = getEpochTimeMs();
  readData(doc);

  // Publish payload to the MQTT topic
  client.beginMessage(topic);
  serializeJson(doc, output);
  client.endMessage();

  // Uncomment to log published message to Serial Monitor
  // Serial.print("Published message to [");
  // Serial.print(topic);
  // Serial.print("]: ");
  // serializeJson(doc, Serial);
  // Serial.println();

  // Send data at 1000 ms interval (1 Hz)
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