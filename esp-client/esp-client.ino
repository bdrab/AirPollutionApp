#include <WiFi.h>
#include <HTTPClient.h>
#include "ESPDateTime.h"
#include "secret.h"
#include <ArduinoJson.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

DynamicJsonDocument doc(1024);
Adafruit_BME280 bme;


String value_data;
  
// "secret.h" file contains secret detail in below format:
//const char* serverName = "";
//const char* ssid = "";
//const char* password = "";


unsigned long lastTime = 0;
unsigned long timerDelay = 900000;

int incomingByte = 0; 
const int MAX_FRAME_LEN = 64;
char frameBuf[MAX_FRAME_LEN];
int detectOff = 0;
int frameLen = MAX_FRAME_LEN;
bool inFrame = false;
char printbuf[256];
unsigned int calcChecksum = 0;
struct PMS7003_framestruct {
    byte  frameHeader[2];
    unsigned int  frameLen = MAX_FRAME_LEN;
    unsigned int  concPM1_0_CF1;
    unsigned int  concPM2_5_CF1;
    unsigned int  concPM10_0_CF1;
    unsigned int  checksum;
} thisFrame;


//void setupDateTime() {
//  DateTime.setServer("0.pl.pool.ntp.org");
//  DateTime.setTimeZone("CET-1CEST,M3.5.0,M10.5.0/3");
//  DateTime.begin();
//  if (!DateTime.isTimeValid()) {
//    Serial.println("Failed to get time from server.");
//  } else {
//    Serial.printf("Date Now is %s\n", DateTime.toISOString().c_str());
//    Serial.printf("Timestamp is %ld\n", DateTime.now());
//  }
//}

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
  bme.begin(0x76);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
//  setupDateTime();
}


void loop() {
  pms7003_read();
  float PM1 = thisFrame.concPM1_0_CF1;
  float PM2_5 = thisFrame.concPM2_5_CF1;
  float PM10 = thisFrame.concPM10_0_CF1;
  
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    value_data = "";
    doc.clear();
//    doc["time"] = String(DateTime.toISOString());
    doc["data"]["sensor"] = 1;
    doc["data"]["pm1"] = thisFrame.concPM1_0_CF1;
    doc["data"]["pm25"] = thisFrame.concPM2_5_CF1;
    doc["data"]["pm10"] = thisFrame.concPM10_0_CF1;
    doc["data"]["temperature"] = bme.readTemperature();
    doc["data"]["pressure"] = bme.readPressure();
    doc["data"]["humidity"] = bme.readHumidity();

    serializeJson(doc, value_data);
    Serial.println(value_data);
    if(WiFi.status()== WL_CONNECTED){
      String data_to_sent =  DateTime.toISOString().c_str();
      WiFiClient client;
      HTTPClient http;
      http.begin(client, serverName);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(value_data);
      Serial.print("HTTP Response code: ");
      Serial.print(httpResponseCode);
      Serial.print("Response: ");
      Serial.println(http.getString());
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
      WiFi.begin(ssid, password);
    }
    lastTime = millis();
  }
}
