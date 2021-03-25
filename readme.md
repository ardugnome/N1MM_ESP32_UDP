NOT FOR COMMERCIAL USE !

Credit for original code to https://github.com/gabrielonet/N1MM

2/17/2021

N1MM software:-

N1MM antenna/band selector based on UDP broadcast on port 12060.
Configuration found in N1MM>Config>ConfigPorts>BroadcastData

"Radio" field needs to be checked in N1MM for UDP broadcast to start, and your home IP broadcast address entered in the N1MM configurer.  

https://n1mmwp.hamdocs.com/setup/the-configurer/


Hardware:-

Assumes you already have the Ameritron RCS-4 remote controlled coax switch.

(This unit replaces the original Ameriton controller head unit, the Ameriton relay box remains the same.)

(Can be configured as a standalone wireless antenna switch with additional hardware.)

Uses the original Ameriton 12vAC power supply that was packaged with the RCS-4 switch.

ESP-32 DEVKIT board 30 or 36 pin.

4 relay board (5V) with low trigger current, 2-4 mA to be driven from the ESP32 pins directly.

OLED SSD1306 0.96 in. 128x64 display, also works with 0.91in 128x32

OLED 3D printed screen cover, plastic, or machine your own.

Metal or plastic, enclosure, mine is from Jameco.

Four position rotary switch or encoder (if you choose the encoder you have to code your own code)

Two SO239 panel mount connectors.

Two SPST miniature switches.

Dc/Dc converter preferred,  or 7-9v regulator with a proper heatsink!!! 

Disc and electrolitic capacitors, diodes, rf choke, fuse, etc. per original RCS-4 schematic (we re-create the power supply (12vAC, -12vDC and +12vDC) from the original Ameriton 
Controller)

Standoffs, screws, pcb headers wires and related mounting hardware.

Front panel labels, lettering or laser printing.

Copper shield if desired.


Python Software:-

Download Thonny from https://thonny.org and set RUN>SELECT INTERPRETER> MicroPython (ESP32) and corresponding COM port to upload files to the ESP32.


N1MM_ESP-32_UDP software:-

Coded in MicroPython (Python) for the ESP 32 Wroom board DEVKITV1 (30 pin version) 

The band decoder option uses the following pins:
(13,14,18,19,23,25,26,27,32,33 (and 21 ,22 if you sacrifice the display))


Installation Files (load them to your ESP32 board using Thonny)

WiCS-4.py   -main program file (rename main.py when all is working to your satisfaction)

ssd1306.py  -OLED display driver file with 03c as display address.

gfx.py      -GFX graphics library

i2c_scan    -good for finding out your OLED's address

Inside WiCS-4.py replace the "SSID" and "pass" with your own WiFi credentials.

If you have the OLED attached run i2c_scan.py to make sure your display's address is 03c.
Make any adjustments to the antenna names as desired and run WiCS-4.py

When finished testing, rename the WiCS-4.py file to main.py to start at boot.


Features: 

Band change (160-6m) less 5Mhz, 144, 222 and 432MHz. Pulls pin high, corresponding to "relay" 1-10 for band decoder output.
Pins for 2m and 432 are used to drive the OLED and should not be used unless you do not inteito have a screen.

Antenna change in automatic mode: flip the switch to auto mode and toggle antennas with Alt+F9 in N1MM *see note below
*Requires internet connection with your home WiFi, assuming N1MM is configured properly to broadcast UDP and is running, the antenna/band combination needs to be set up correctly in N1MM>Config>ConfigPorts>Antennas

Antenna change in manual mode: flip manual/auto to manual, and rotate the knob to desired antenna. 

Radio number 1 vs 2 as decoded from UDP stream. (Not used yet)


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



Update: 3/22/21

Added OLED code based on ssd1306 display.

Changed OLED from 128x32 (0.91in) to 128x64 (0.96in), both will work, but 128x64 looks bigger.

Added rssi information on the screen to monitor Wifi signal strength. 

Added frequency information on the screen in auto mode(user has to choose between rssi and freq), currently only rssi is dispayed.

Added manual mode when N1MM is not running.

Added code to switch between auto and manual modes.

Added photos of completed WiCS-4 antenna switch.

Added schematic diagram.


Known issues:


Band decoder option requires the pins mentioned in the code brought to a DB-15 connector or other header (DB-25, in-line, terminal block)

When changing from Manual to Auto there is a long wait.

In Auto mode if N1MM is not started or there is no internet connection or N1MM is started before the WiCS-4 the two may not connect. Reboot N1MM.


Final thoughts.

I'm sure the program can be cleaned up a lot by someone with a lot more experience.
EULA. This program is free for non commercial use, with no warranty expressed or implied, all these experiments are at your own risk, I cannot be held responsible for any damages. USE OF THIS SOFTWARE/HARDWARE CONSTITUTES ACCEPTANCE OF THIS AGREEMENT. 
