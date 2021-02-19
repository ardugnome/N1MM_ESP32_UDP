Credit for original code to https://github.com/gabrielonet/N1MM

N1MM band selector based on UDP port 12060 found in N1MM>Config>ConfigPorts>BroadcastData

Radio field needs to be checked in N1MM 

Make sure you have a space between the first and second IP, and replace the x with your home net address in N1MM

Replace the "SSID" and "pass" with your own WiFi credentials

Coded in MicroPython (Python) for ESP 32 Wroom board DEVKITV1 (30 pin) - for relay command use only pins 13,14,18,19,23,25,26,27,32,33 (and 21 ,22 if you sacrifice I2C)

You need a blue board or transistors to drive relays, do not drive them from the ESP32 pins directly

You may rename the .py file to main.py to start at boot if you know what you're doing.

Download Thonny from https://thonny.org and set RUN>SELECT INTERPRETER> MicroPython (ESP32) and corresponding COM port


Features: 

Band change (160-70cm) less 5Mhz and 222 MHz  activate a pin corresponding to relay 1-12

Antenna change  *see note below
*Antenna change is done by pressing ALT+F9 in N1MM if the antennas and bands were set up in N1MM>Config>ConfigPorts>Antennas

Radio change (Radio1 vs. Radio2) for SO2R


For more information on N1MM:  https://n1mmwp.hamdocs.com/

For more information on UDP XML: https://n1mmwp.hamdocs.com/appendices/external-udp-broadcasts

Typical output:

N1MM UDP server up and listening on port ('IP Address', 'port number#')

160 meters band, Relay # 1 Radio#: 1 Antenna#: 0

80 meters band, Relay # 2 Radio#: 1 Antenna#: 0

40 meters band, Relay # 3 Radio#: 1 Antenna#: 0

40 meters band, Relay # 3 Radio#: 1 Antenna#: 2

20 meters band, Relay # 5 Radio#: 1 Antenna#: 0

20 meters band, Relay # 5 Radio#: 1 Antenna#: 1



Reccomended pin use from here: https://www.electronicshub.org/esp32-pinout/

2/17/2021 NJ9R
