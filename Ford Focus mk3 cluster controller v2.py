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

id_counter = 0x0

rpm = 2000
speed = 6108
coolant_temp = 120
fuel = 50

left_directional = True
right_directional = False
tc = False
abs = False
battery = False

outside_temp = 72

while True:
    current_time = time.time()
    
    ready_to_read, _, _ = select.select([sock], [], [], 0)
    if sock in ready_to_read:
        data, _ = sock.recvfrom(256)
        packet = struct.unpack('I4sH2c7f2I3f16s16si', data)
        rpm = int(max(min(packet[6], 8000), 0))
        speed = max(min(int(packet[5]*358), 24200), 0) #convert speed to km/h
        left_directional = False
        right_directional = False
        if (packet[13]>>5)&1:
            left_directional = True
            print("LDIR")
        if (packet[13]>>6)&1:
            right_directional = True
    # Execute code every 100ms
    elapsed_time_100ms = current_time - start_time_100ms
    if elapsed_time_100ms >= 0.1:
        messages_100ms = [
            
            can.Message(arbitration_id=0x3a, data=[ # Directionals
                0x03,(right_directional*8) + (left_directional*4),0x01,0xff,0x81,0xff,0xff,0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x40, data=[ # Airbag light, odometer increment
                0,0,0,0,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x60, data=[ # Seatbelt
                0xd0,0,0,0,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x70, data=[ # ABS/TC
                0x00,0x95,0x04,0x82,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x80, data=[ #Ignition, Doors, Parking Lights, Cruise Control
                0x44,0b10000111,0x07,0b00000000,0,0b10101010,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1a4, data=[ # Outside Temp
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1a8, data=[ # Highbeam, Rear Foglight, HDC, Brakelight
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x1b0, data=[ # Foglight
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x230, data=[ # TPMS
                0x0,0x95,0x04,0x82,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x250, data=[ # Oil Pressure, MIL, Backlight Brightness
                0xFF,0x10,0,0,0,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x290, data=[ # Brake fluid error message (from ECU?)
                0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x2a0, data=[ # Engine service (?)
                0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x300, data=[ # Trans. Malfunction, Battery light
                0,0,0,0,0xff,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x320, data=[ #Fuel 
                0x33,0x33,0x33,0x33,0xff,0x33,0x33,0x33], is_extended_id=False),
            
            can.Message(arbitration_id=0x360, data=[ # Engine Temp
                0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa,0xaa], is_extended_id=False),
            
            can.Message(arbitration_id=0x466, data=[ # Compass
                0xff,0xff,0x00,0x22,0x50,0xff,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=id_counter, data=[
                random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)], is_extended_id=False),
        ]
        
        for message in messages_100ms:
            bus.send(message)
            #print(message)
            wpt.sleep(0.005)
        start_time_100ms = time.time()


    # Execute code every 10ms
    elapsed_time_10ms = current_time - start_time_10ms
    if elapsed_time_10ms >= 0.01:  # 10ms
        messages_10ms = [
            can.Message(arbitration_id=0x110, data=[ 
                0xff,0xff,0,0,(int(rpm/2))>>8,(int(rpm/2))&0xff,(speed&0xff00)>>8,speed&0xff], is_extended_id=False),
            
            can.Message(arbitration_id=0x290, data=[
                0xFF,0,0,0,0b10101010,0,0,0], is_extended_id=False),
            
            can.Message(arbitration_id=0x20, data=[ # Directionals
                1,1,1,0,0x81,0xff,0xff,random.randint(0,255)], is_extended_id=False),
            
        ]
        
        for message in messages_10ms:
            bus.send(message)
            wpt.sleep(0.001)
        start_time_10ms = time.time()

    # Execute code every 5s
    elapsed_time_5s = current_time - start_time_5s
    if elapsed_time_5s >= 3:
        #id_counter += 1
        print(hex(id_counter))
        start_time_5s = time.time()

sock.close()

