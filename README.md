# Ford Focus MK3 Cluster Controller w/ ESP32 or python-can
Scripts to control the Ford Focus MK3 Instrument Cluster {P/N:CM5T-10849-TU) with an ESP32-WROOM module and an SN65HVD230 CAN bus tranceiver or with any python-can compatible interface. 
I used a color LCD cluster but this should also work with the smaller and monochrome LCD cluster.
CAN Speed is 125kbps and serial speed is 115200 baud

Arduino code will probably be missing features compared to the python one as i no longer have the hardware to test it

# WHAT WORKS:
- Speedometer
- RPM (perfect)
- All red error messages gone
- Outside Temp

# WHAT DOES NOT WORK:
- red brake light always on
- Glowplug Light
- Auto Start/Stop Light
- LDA Light
- cant get rid of starter malfunction error

# Found message ID, unknown bytes or i didnt implement it yet
- Check Engine Light
- Oil Pressure Light 
- Engine Temp 
- TPMS Light
- ABS Light
- TC/TC Off Light
- Directionals
- Highbeam
- Fog Light
- Cruise Control
- Set Backlight Brightness

More notes are in notes.txt
