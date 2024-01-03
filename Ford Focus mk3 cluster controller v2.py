import time
import can
import random
import socket
import struct
import select 
import win_precise_time as wpt

bus = can.interface.Bus(channel='com11', bustype='seeedstudio', bitrate=125000)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 4444))
    
# Track time for each function separately
start_time_100ms = time.time()
start_time_10ms = time.time()
start_time_5s = time.time()

id_counter = 0x81

rpm = 2000
speed = 6108
coolant_temp = 120
fuel = 50

left_directional = True
right_directional = True
tc = False
abs = False
battery = False
handbrake = False
highbeam = True

#not recved by outgauge but works on cluster
outside_temp = 72
compass = 0x30
# N = ?
# NE = ?
# E = ?
# SE = ?
# S = ?
# SW = ?
# W = ?
# NW = ?

hdc = False
tpms = False
cruise_control = False
cruise_control_speed = 80
foglight = True
parking_lights = False
rear_foglight = False # works
check_engine = False
driver_door = False
passenger_door = False
driver_rear_door = False
passenger_rear_door = False
hood = False
trunk = False
front_left = 30
front_right = 30
rear_left = 30
rear_right = 30
engine_malfunction = False
transmission_temp = 100
airbag = False
seatbelt = False

while True:
    current_time = time.time()
    
    #read from the socket if there is data to be read
    ready_to_read, _, _ = select.select([sock], [], [], 0)
    if sock in ready_to_read:
        data, _ = sock.recvfrom(256)
        packet = struct.unpack('I4sH2c7f2I3f16s16si', data)
        
        rpm = int(max(min(packet[6], 8000), 0))
        speed = max(min(int(packet[5]*358), 24200), 0) #convert speed to km/h
        
        left_directional = False
        right_directional = False
        highbeam = False
        abs = False
        battery = False
        tc = False
        handbrake = False
        
        if (packet[13]>>1)&1:
            highbeam = True
        if (packet[13]>>2)&1:
            handbrake = True
        if (packet[13]>>4)&1:
            tc = True
        if (packet[13]>>10)&1:
            abs = True
        if (packet[13]>>9)&1:
            battery = True
        if (packet[13]>>5)&1:
            left_directional = True
        if (packet[13]>>6)&1:
            right_directional = True
            
    # Send each message every 100ms
    elapsed_time_100ms = current_time - start_time_100ms
    if elapsed_time_100ms >= 0.1:
        messages_100ms = [
            
            can.Message(arbitration_id=0x3a, data=[ # Directionals
                0x03,(right_directional*8) + (left_directional*4),0x01,0xff,0x81,0xff,0xff,0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x40, data=[ # Airbag light, odometer increment
                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=False),
            
            can.Message(arbitration_id=0x60, data=[ # Seatbelt
                0xd0,0,0,0,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x70, data=[ # ABS/TC
                0x00, 0x98, 0x4, 0x80, 0x00, 0xF4, 0xE8, 0x10], is_extended_id=False),
            
            can.Message(arbitration_id=0x80, data=[ # Ignition, Doors, Parking Lights, Cruise Control
                0x44,0b10000111,0x07,0x3e,0xd9,0x06,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1a4, data=[ # Outside Temp
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1a8, data=[ # Highbeam, Rear Foglight, HDC, Brakelight
                0,(highbeam),(rear_foglight*64),0x22,0x00,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1b0, data=[ # Foglight
                0xff,0xff,(foglight*8),0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1e0, data=[ # Immobilizer
                0x4A, 0x88, 0x3C, 0x00, 0x00, 0xC0, 0x80, 0x00], is_extended_id=False),
            
            can.Message(arbitration_id=0x230, data=[ # TPMS
                0x0,0x95,0x04,0x82,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x240, data=[ # water in fuel message
                0xF5, 0x00, 0x00, 0x40, 0x00, 0x9F, 0x80, 0xD1], is_extended_id=False),
            
            can.Message(arbitration_id=0x250, data=[ # Oil Pressure, MIL, Backlight Brightness
                0xFF, 0x10, 0x15, 0x03, 0x14, 0x10, 0x0E, 0x31], is_extended_id=False),
            
            can.Message(arbitration_id=0x290, data=[ # Brake fluid error message (from ECU?)
                0x93, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x13], is_extended_id=False),
            
            can.Message(arbitration_id=0x2a0, data=[ # Engine service (?)
                70, 0xFF, 0x80, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], is_extended_id=False),
            
            can.Message(arbitration_id=0x300, data=[ # Trans. Malfunction, Battery light
                0,0,0,0,0xff,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x320, data=[ #Fuel 
                0xe, 0xe, 30, 0, 0xe, 0xe, 0xe, 0xe], is_extended_id=False),
            
            can.Message(arbitration_id=0x360, data=[ # Engine Temp
                0x00, 0x00, 0x00, 0x22, 0x46, 0xFE, 0x22, 0x22], is_extended_id=False),
            
            can.Message(arbitration_id=0x466, data=[ # Compass
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=id_counter, data=[
                random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)], is_extended_id=False),
        ]
        
        for message in messages_100ms:
            bus.send(message)
            #print(message)
            wpt.sleep(0.007)
        start_time_100ms = time.time()


    # Execute code every 10ms
    elapsed_time_10ms = current_time - start_time_10ms
    if elapsed_time_10ms >= 0.01:  # 10ms
        messages_10ms = [
            can.Message(arbitration_id=0x110, data=[ 
                0xff,0xff,0,0,(int(rpm/2))>>8,(int(rpm/2))&0xff,(speed&0xff00)>>8,speed&0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x290, data=[
                0xFF,0,0,0,0b10101010,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x20, data=[ # Gear
                0x00, 0x00, 0x1, 0x00, 0x1, 0x00, 0x00, 0x00], is_extended_id=False),
            
        ]
        
        for message in messages_10ms:
            bus.send(message)
            wpt.sleep(0.001)
        start_time_10ms = time.time()

    # Execute code every 5s
    elapsed_time_5s = current_time - start_time_5s
    if elapsed_time_5s >= 3:
        id_counter += 1
        print(hex(id_counter))
        start_time_5s = time.time()

sock.close()

