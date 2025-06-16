#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define NUM_SENSORS 5
DeviceAddress sensorAddresses[NUM_SENSORS] = {
  { 0x28, 0xD1, 0xE2, 0x52, 0x00, 0x00, 0x00, 0x6B }, // Glycol
  { 0x28, 0x31, 0x0A, 0x52, 0x00, 0x00, 0x00, 0xA6 }, // Preheat
  { 0x28, 0xF9, 0xAF, 0x51, 0x00, 0x00, 0x00, 0xF1 }, // Ambient
  { 0x28, 0x25, 0x8C, 0x50, 0x00, 0x00, 0x00, 0x71 }, // Source
  { 0x28, 0xC7, 0xC0, 0x50, 0x00, 0x00, 0x00, 0xFE }  // Hot
};

// Data wire is connected to GPIO 15
#define ONE_WIRE_BUS 15

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();

  delay(750);

  for (int i = 0; i < NUM_SENSORS; i++) {
    float tempC = sensors.getTempC(sensorAddresses[i]);
    Serial.print("Temperature Sensor ");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(tempC);
    Serial.println("°C");
  }

  delay(5000);
}
