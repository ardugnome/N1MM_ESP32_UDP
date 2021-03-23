Credit for original code to https://github.com/gabrielonet/N1MM

N1MM antenna/band selector based on UDP port 12060 found in N1MM>Config>ConfigPorts>BroadcastData

"Radio" field needs to be checked, and your home IP broadcast address entered in N1MM configurator.  

Replace the "SSID" and "pass" with your own WiFi credentials.

Coded in MicroPython (Python) for ESP 32 Wroom board DEVKITV1 (30 pin) - for relay command use only pins 13,14,18,19,23,25,26,27,32,33 (and 21 ,22 if you sacrifice display)

You need a 4 relay board with low trigger current, 2-4 mA to drive them from the ESP32 pins directly.

When finished testing, rename the WiCS-4.py file to main.py to start at boot.

Download Thonny from https://thonny.org and set RUN>SELECT INTERPRETER> MicroPython (ESP32) and corresponding COM port to upload files to the ESP32.

Files:
WiCS-4.py   -main program file
ssd1306.py  -OLED display driver file
gfx.py      -GFX graphics library

Features: 

Band change (160-6m) less 5Mhz, 144, 222 and 432MHz  pulls high a pin corresponding to relay 1-10 for your band decoder
Pins for 2m and 432 are used to drive the OLED

Antenna change in automatic mode: flip the switch to auto mode and have N1MM broadcast UDP *see note below
*Requires internet connection with your home WiFi, antenna change is done by pressing ALT+F9 in N1MM assuming the antenna/band combination was set up correctly in N1MM>Config>ConfigPorts>Antennas

Antenna change in manual mode: flip manual/auto to manual, and rotate the knob to desired antenna. 

Radio change (Radio1 vs. Radio2) for SO2R is being broadcasted by N1MM


For more information on N1MM:  https://n1mmwp.hamdocs.com/

For more information on UDP XML: https://n1mmwp.hamdocs.com/appendices/external-udp-broadcasts

Typical debug output:

N1MM UDP server up and listening on port ('IP Address', 'port number#')

160 meters band, Relay # 1 Radio#: 1 Antenna#: 0

 80 meters band, Relay # 2 Radio#: 1 Antenna#: 0
 
 40 meters band, Relay # 3 Radio#: 1 Antenna#: 0
 
 40 meters band, Relay # 3 Radio#: 1 Antenna#: 2
 
 20 meters band, Relay # 5 Radio#: 1 Antenna#: 0
 
 20 meters band, Relay # 5 Radio#: 1 Antenna#: 1



Reccomended pin use from here: https://www.electronicshub.org/esp32-pinout/

2/17/2021

Update: 3/22/21

Added OLED code based on ssd1306 display.

Changed OLED from 128x32 to 128x64, both will work, but 128x64 looks bigger.

Added rssi information on the screen to monitor Wifi signal strength.

Added frequency information on the screen in auto mode(user has to choose between rssi and freq).

Added manual mode when N1MM is not running.

Added code to switch between auto and manual modes.

Added photos of completed WiCS-4 antenna switch.


Known issues:

When changing from Manual to Auto there is a long wait.

In Auto mode if N1MM is not started or there is no internet connection or N1MM is started before the WiCS-4 the two may not connect. Reboot N1MM.
