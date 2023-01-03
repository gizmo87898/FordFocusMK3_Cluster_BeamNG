// Copyright (c) Sandeep Mistry. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

#include <CAN.h>
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <WiFi.h>

#define lo8(x) ((int)(x)&0xff)
#define hi8(x) ((int)(x)>>8)

//CAN loop coutners
unsigned long sinceLast100msLoop = 0;
unsigned long sinceLast200msLoop = 0;
unsigned long sinceLast1000msLoop = 0;
unsigned long sinceLast5sLoop = 0;


int speed = 20;
int rpm = 3000;

void setup() {
  // Begin serial at 115200bps
  Serial.begin(115200);
  // Set CAN RX/TX pins to 2 and 15
  CAN.setPins(15,2);
  // start the CAN bus at 125 kbps
  if (!CAN.begin(125E3)) {
    Serial.println("Starting CAN failed!");
    while (1);
  }
  Serial.println("Initialized");
}


void loop() {
  unsigned long currentLoop = millis();
  String data;                                                                                                                                                                                                                                                                                                                                 
  int packetSize = CAN.parsePacket();
  if (packetSize) { 
    // if a packet is present
    while (CAN.available()) {
      data.concat(String(CAN.read(), HEX));
    }
    Serial.print("id: 0x");
    Serial.print(CAN.packetId(), HEX);
    Serial.print(" DLC: ");
    Serial.print(packetSize);
    Serial.print("  data: ");
    Serial.println(data);
      
  }
  if (currentLoop - sinceLast100msLoop > 100) {
    sinceLast100msLoop = currentLoop;
    send80();
    send110();
    if(rpm > 8000) {
      rpm = 0;
    }
    rpm+=30;
    if(speed > 150) {
      speed = 0;
    }
    speed+=1;
  }
  if (currentLoop - sinceLast200msLoop > 200) {
    sinceLast200msLoop = currentLoop;
  }
  if (currentLoop - sinceLast1000msLoop > 1000) {
    sinceLast1000msLoop = currentLoop;
  }
  if (currentLoop - sinceLast5sLoop > 5000) {
    sinceLast5sLoop = currentLoop;
  }
}

void send80() {
    CAN.beginPacket(0x080);
    CAN.write(0x44);
    CAN.write(0x87);
    CAN.write(0x07);
    CAN.write(0b00101010);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.endPacket();
    Serial.println("0x80 Sent");
}
void send110() {
    CAN.beginPacket(0x110);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(hi8(rpm/2)); // rpm highbyte
    CAN.write(lo8(rpm/2)); // rpm lowbyte
    CAN.write(speed/1.6); // speed highbyte
    CAN.write(lo8(speed/1.6)); // speed decimal
    CAN.endPacket();
    Serial.println("0x110 Sent");
}
