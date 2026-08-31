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
char topic[] = "coursecode/ltuXX";  // e.g. D0022B/ltu11

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

  while (!client.connect(broker, port)) {
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
