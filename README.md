# FordFocusMK3_Cluster_ESP32
A short arduino script to controll the Ford Focus MK3 Instrument Cluster {P/N:CM5T-10849-TU) with an ESP32-WROOM module with a SN65 something CAN bus tranceiver. This can also be done with a lil bit different code on an Atmega328p/whatever else with a MCP2515 CAN controller and tranciever, only a tranciever is needed on this since the ESP32 has a built in CAN controller.
# WHAT WORKS:
- Speedometer
- RPM
- Engine Temp 
- MIL (check engine light)
- Oil Pressure Light
- TPMS Light
- ABS Light
- TC/TC Off Light

# WHAT DOES NOT WORK:
-
