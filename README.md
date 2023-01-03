# Ford Focus MK3 Cluster Controller with an ESP32
A short arduino script to control the Ford Focus MK3 Instrument Cluster {P/N:CM5T-10849-TU) with an ESP32-WROOM module with a SN65HVD230 CAN bus tranceiver. This can also be done with a lil bit different code on an Atmega328p/whatever else with a MCP2515 CAN controller and tranciever, only a tranciever is needed on this since the ESP32 has a built in CAN controller.
I used a color LCD cluster but this should also work with the smaller and monochrome LCD cluster.
CAN Speed is 125kbps and serial speed is 115200 baud

# WHAT WORKS:
- Speedometer
- RPM
- Engine Temp 
- MIL (check engine light)
- Oil Pressure Light
- TPMS Light
- ABS Light
- TC/TC Off Light
- Directionals (not added yet)
- Highbeam (not added yet)
- Cruise Control (somewhat)
- Set Backlight Brightness


# WHAT DOES NOT WORK:
- Brake Light
- Glowplug Light
- Auto Start/Stop Light
- LDA Light

# More IDs:
These are IDs I found while bruteforcing random data.
id (in dec) - description

- 58 - directionals
- 64 - airbag
- 96 - seatbelt light
- 112 - abs / trac ctrl
- 128 - parking lights, doors, cruise ctrl
- 272 - speed and rpm
- 420 - outside temp
- 424 - highbeam, orange foglight, hdc, brake light status
- 432 - foglight
- 560 - tpms
- 592 - oil press. mil, backlight
- 657 - brake fluid messgae, trans overheat message, steering assist message
- 768 - trans malfunction, battery light
- 800 - made fuel gauge twitch
- 864 - eng temp
