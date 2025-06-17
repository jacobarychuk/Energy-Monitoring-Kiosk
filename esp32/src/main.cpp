#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "secrets.h"

#define NUM_SENSORS 5
DeviceAddress sensorAddresses[NUM_SENSORS] = {
  { 0x28, 0xD1, 0xE2, 0x52, 0x00, 0x00, 0x00, 0x6B }, // Glycol
  { 0x28, 0x31, 0x0A, 0x52, 0x00, 0x00, 0x00, 0xA6 }, // Preheat
  { 0x28, 0xF9, 0xAF, 0x51, 0x00, 0x00, 0x00, 0xF1 }, // Ambient
  { 0x28, 0x25, 0x8C, 0x50, 0x00, 0x00, 0x00, 0x71 }, // Source
  { 0x28, 0xC7, 0xC0, 0x50, 0x00, 0x00, 0x00, 0xFE }  // Hot
};
const String sensorNames[NUM_SENSORS] = {
  "glycol",
  "preheat",
  "ambient",
  "source",
  "hot"
};

// Data wire is connected to GPIO 15
#define ONE_WIRE_BUS 15

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();

  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nConnected! IP Address: ");
  Serial.println(WiFi.localIP());

  configTime(-28800, 3600, "time.google.com");
  Serial.print("Synchronizing time...");
  time_t now = time(nullptr);
  while (now < 100000) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.print("\nSynchronized! Time: ");
  Serial.println(time(nullptr));
}

void loop() {
  sensors.requestTemperatures();

  delay(750);

  String json = "{\"timestamp\": " + String((uint64_t) time(nullptr)) + ",";

  for (int i = 0; i < NUM_SENSORS; i++) {
    float tempC = sensors.getTempC(sensorAddresses[i]);

    json += "\"" + sensorNames[i] + "\": " + String(tempC);

    if (i < NUM_SENSORS - 1) {
      json += ",";
    }
  }

  json += "}";

  HTTPClient http;
  http.begin("http://raspberrypi.local:5000/data");
  http.addHeader("Content-Type", "application/json");
  http.POST(json);
  http.end();

  delay(5000);
}
