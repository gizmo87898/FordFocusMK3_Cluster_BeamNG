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
- Directionals
- Highbeam
- Fog Light
- Cruise Control (somewhat)
- Set Backlight Brightness
- All red error messages gone
- Outside Temp
- Compass (not added yet)

# WHAT DOES NOT WORK:
- Brake Light
- Glowplug Light
- Auto Start/Stop Light
- LDA Light
- Some warnings still appear
- Fuel Gauge

More notes are in notes.txt
