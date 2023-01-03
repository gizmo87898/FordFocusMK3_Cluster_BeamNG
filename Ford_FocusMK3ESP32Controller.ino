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

int speed = 0;
int rpm = 0;

// for needle sweeper
bool rpmForward = true;
bool speedForward = true;

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
    send20(); // Unknown
    send40(); // Airbag
    send70(); // ABS
    send80(); // Ignition Status
    send110(); // RPM and Speed
    send230(); // TPMS
    send250(); // ECU
    send2a0(); // Engine Service 
    send300(); // Alternator light
    send360(); // Engine Temp
    
    // RPM Needle sweeper
    if (rpm >= 8000) {
      rpmForward = false;
    }
    if (rpm <= 0) {
      rpmForward = true;
    }
    if (rpmForward) {
      rpm +=200;
    }
    else {
      rpm = rpm - 200;
    }
    
    // Speed needle sweeper
    if (speed >= 150) {
      speedForward = false;
    }
    if (speed <= 0) {
      speedForward = true;
    }
    if (speedForward) {
      speed += 1;
    }
    else {
      speed = speed - 1;
    }
  }
}
void send20() { // Dont really know what this does but it was in a log
  CAN.beginPacket(0x020);
  CAN.write(0x03);
  CAN.write(0xc1);
  CAN.write(0x01);
  CAN.write(0xff);
  CAN.write(0x81);
  CAN.write(0xff);
  CAN.write(0xff);
  CAN.write(0xff);
  CAN.endPacket();
  Serial.println("0x20 Sent");
}
void send40() { // Airbag
    CAN.beginPacket(0x040);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.endPacket();
    Serial.println("0x40 Sent");
}
// 0x70
// byte1 - tc status
// 0b10101010 - "tc off" on
// 0b11000000 - "tc off" on
// 0010000000 - both tc lights on
void send70() { // ABS
    CAN.beginPacket(0x070);
    CAN.write(0x00);
    CAN.write(0x95);
    CAN.write(0x04);
    CAN.write(0x82);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.endPacket();
    Serial.println("0x70 Sent");
}
void send80() { // Ignition Status
    CAN.beginPacket(0x080);
    CAN.write(0x44);
    CAN.write(0b10000111);
    CAN.write(0x07);
    CAN.write(0b00000000);
    CAN.write(0x00);
    CAN.write(0b10101010);
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
    CAN.write(lo8(speed)); // speed decimal ?
    CAN.endPacket();
    Serial.println("0x110 Sent");
}
void send230() {
    CAN.beginPacket(0x230);
    CAN.write(0x00);
    CAN.write(0x95);
    CAN.write(0x04);
    CAN.write(0x82);
    CAN.write(0x00); 
    CAN.write(0x00);
    CAN.write(0x00); 
    CAN.write(0x00);
    CAN.endPacket();
    Serial.println("0x230 Sent");
}
void send250() {
    CAN.beginPacket(0x250);
    CAN.write(0xFF);
    CAN.write(0x10);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00); 
    CAN.write(0x00); 
    CAN.write(0x00); 
    CAN.write(0x00);
    CAN.endPacket();
    Serial.println("0x250 Sent");
}
void send2a0() {
    CAN.beginPacket(0x2a0);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0xFF);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.write(0xff);
    CAN.endPacket();
    Serial.println("0x2a0 Sent");
}
void send300() {
    CAN.beginPacket(0x300);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0xff);
    CAN.write(0x00);
    CAN.write(0x00);
    CAN.write(0x00); 
    CAN.endPacket();
    Serial.println("0x300 Sent");
}
void send360() {
    CAN.beginPacket(0x360);
    CAN.write(0x33);
    CAN.write(0x33);
    CAN.write(0x33);
    CAN.write(0x33);
    CAN.write(0x33);
    CAN.write(0x33); 
    CAN.write(0x33);
    CAN.write(0x33);
    CAN.endPacket();
    Serial.println("0x360 Sent");
}
