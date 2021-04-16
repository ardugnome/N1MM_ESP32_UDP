#  !!!    NOT FOR COMMERCIAL USE !!!
# ver 1.0
# WiCS-4 is a N1MM band selector based on UDP port 12060 found in N1MM>Config>ConfigPorts>BroadcastData
# Radio field needs to be checked and the following information typed 127.0.0.1:12060 192.x.x.255:12060
# Make sure you have a space between the first and second IP, and replace the x with your home net address
# Also replace the SSID and pass with your own WiFi credentials
# !ESP 32 Wroom board - use only pins 4,13,16,17,18,19,21,22,23,25,26,27,32,33 for relay command
# !you need a blue board or transistors to drive relays, do not drive them from the ESP32 pins
# You can set this file to start at boot by renaming it main.py if you know what you're getting into
#
# Original N1MM code from https://github.com/gabrielonet/N1MM
#
# Print, prints (debug) on your Thony serial display or any other serial monitor such as Arduino
#
import network, usocket, utime, time
import machine
from socket import *
import gfx
from machine import Pin, SoftI2C
#from machine import Pin
import ssd1306
from ssd1306 import SSD1306_I2C
import framebuf
from time import sleep
import errno
gc.enable()

#The pins below can be used for band decoder output

b160 = Pin(13, Pin.OUT)
b160.value(0)

b80 = Pin(14, Pin.OUT)
b80.value(0)

b40 = Pin(27, Pin.OUT)
b40.value(0)

b30 = Pin(26, Pin.OUT)
b30.value(0)

b20 = Pin(25, Pin.OUT)
b20.value(0)

b17 = Pin(33, Pin.OUT)
b17.value(0)

b15 = Pin(32, Pin.OUT)
b15.value(0)

b12 = Pin(23, Pin.OUT)
b12.value(0)

b10 = Pin(19, Pin.OUT)
b10.value(0)

b6 = Pin(18, Pin.OUT)
b6.value(0)

#The pins below are not implemented because are used for OLED but the code is there and will give you an error if you attempt to use it above 6m
#Pin21 and 22 are used for OLED i2c
#Use 2 and 4
b2 = Pin(21, Pin.OUT)
b2.value(0)

b70 = Pin(22, Pin.OUT)
b70.value(0)

station = network.WLAN(network.STA_IF)
station.active(True)
#Enter your own WiFi SSID and Password
station.connect("YOUR_WIFI_SSID", "YOUR_WIFI_Password")
station.isconnected()

while station.isconnected() == False:
  pass

IP =(station.ifconfig()[0])
#If you need to change the port from default of 12060, change it below and in N1MM
localPort = 12060
bufferSize = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

addrs = (IP, localPort)
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(15)
s.bind(addrs)
#The line below is for serial output debugging
print("N1MM UDP server up and listening on port", IP)


# Only uncomment one of the lines below based on your hardware
# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
# OLED initialization for boot time information
# Dispalys logo/name and IP info to add to N1MM
# Even if you use a 128x64 display leave height at 32 because it looks bigger for us old folks
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# Raspbery Pi Logo as 32x32 array for future testing, loads on boot skewed
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
# Load the raspberry pi logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
# Blit the image from the framebuffer to the oled display
oled.blit(fb, 38, 1)
oled.show()
sleep(3)
# WiCS-4 antenna logo, yes it's a 4el beam.HI
ANTENNA = [
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [ 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [ 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [ 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [ 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
oled.fill(0) # Clear the display
for y, row in enumerate(ANTENNA):
    for x, c in enumerate(row):
        oled.pixel(x, y, c)    
#You may change this text to suit your needs
oled.text('WiCS-4 - NJ9R ',15,1)
oled.text('Remote Wi-Fi',1,12)
oled.text('Antenna Switch',1,22)
oled.show()
sleep(3)
oled.fill(0)
oled.text('N1MM Server',1,1)
oled.text(str(IP), 1, 12)
oled.text('UDP Port: '+str(localPort), 1, 22)
oled.show()
sleep(5)
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)


#Pin definition for manual control: 36 (VP), 39(VN), 34 , 35
#Pull each pin up with an external resistor to 3.3v
#You cannot pull them in software because they do not have internal pull-up resistors !
p36 = Pin(36, Pin.IN)
p39 = Pin(39, Pin.IN)
p34 = Pin(34, Pin.IN)
p35 = Pin(35, Pin.IN)

# Antenna placeholder, when things go wrong...
AnT='OOPS...'

# Relay output pins see wiring diagram 
Pin2 = Pin(2, Pin.OUT) # Relay 1
Pin4 = Pin(4, Pin.OUT) # Relay 2
Pin5 = Pin(5, Pin.OUT) # Relay 3
# Make sure all realys are in the off possition(Dummy Load)
Pin2.off(), Pin4.off(), Pin5.off()

       
def manualAntenna():
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    old_ant=99
    
    while(True):
            
            if 1==p36.value() and 1==p39.value() and 1==p34.value() and 1==p35.value():
                print('Auto Antenna while in Manual Mode')
                autoAntenna() 
            
            oled.fill(0)
            oled.text('MANUAL', 1,1)
            rssi=str(station.status('rssi'))
            #graphics.fill_rect(1,1,128,10,1)
            oled.text(rssi+'dBm', 75,10,1)
            
            if 0==p36.value():
                #pos 4 -0v
                ant=3
            elif 0==p39.value():
                #pos3 -12v
                ant=2
            elif 0==p34.value():
                #Pos 2 +12v
                ant=1
            elif 0==p35.value():
                #Pos1 12vAC
                ant=0
            else:
                autoAntenna()
                
            if ant==0:
                #Position 1
                AnT='LONG WIRE'
                Pin2.on()
                sleep(0.1)
                Pin4.on()
                sleep(0.1)
                Pin5.on()
                
            if ant==1:
                #Position 2
                AnT='BEAM'
                Pin2.off()
                sleep(0.1)
                Pin4.off()
                sleep(0.1)
                Pin5.on()
                
            if ant==2:
                #Position 3
                AnT='40m DIPOLE'
                Pin2.off()
                sleep(0.1)
                Pin4.on()
                sleep(0.1)
                Pin5.on()
                
            if ant==3:
                #Position 4
                AnT='DUMMY LOAD'
                Pin2.off()
                sleep(0.1)
                Pin4.off()
                sleep(0.1)
                Pin5.off()
                
            if old_ant !=ant:
                old_ant=ant
            
            graphics.fill_rect(22,20,128,10,0)
            oled.text('Ant: '+AnT, 1,20,1)
            oled.show()
            
             
def autoAntenna():
    oled.fill(0)
    oled.show()
    freq_temp = 0
    radio_temp = 0
    ant_temp = 0
    try:
        while(True):
            if 0==p36.value() or 0==p39.value() or 0==p34.value() or 0==p35.value():
                    print('Manual Antenna')
                    manualAntenna() 
            rssi=str(station.status('rssi'))
            graphics.fill_rect(75,10,128,10,0)
            oled.text(rssi+'dBm', 75,10,1)
            oled.show()
            bytesAddressPair = s.recvfrom(bufferSize) 
            message = bytesAddressPair[0]
            clientMsg = "Message from Client:{}".format(message)             
            parser1 = clientMsg.split("</Freq")[0]  
            freq = int(float(parser1.split("Freq>")[1])) 
            parser2 = clientMsg.split("</RadioNr")[0]  
            radio = int(int(parser2.split("RadioNr>")[1]))
            parser3 = clientMsg.split("</Antenna")[0]  
            ant = int(int(parser3.split("Antenna>")[1]))
            #print('in Auto loop')
            if radio !=radio_temp or ant !=ant_temp or freq != freq_temp:
                #need to add pin change above to work outside N1MM 
                freq_temp = freq
                ant_temp=ant
                radio_temp=radio
                band=0
                #Display ham bands and band decoder
                if 179999 < freq < 200000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b160.value(1)             
                    band='160'
                    print (band+" meters band, MCU:",str(b160)+" Radio#:", radio, "N1MM Antenna#:", ant)       
                if 349999 < freq < 400000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b80.value(1)
                    band='80'
                    print(band+" meters band, MCU:",str(b80)+" Radio#:", radio, "Antenna#:", ant) 
                if 533050 < freq < 540350:
                    band='60'    
                    
                if 699999 < freq < 730000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b40.value(1) 
                    band='40'
                    print(band+" meters band, MCU:",str(b40)+" Radio#:", radio, "Antenna#:", ant)
                if 1010000 < freq < 1015000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b30.value(1)
                    band='30'
                    print(band+" meters band, MCU:",str(b30)+" Radio#:", radio, "Antenna#:", ant)
                if 1399999 < freq < 1435000: 
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b20.value(1)
                    band='20'
                    print(band+" meters band, MCU:",str(b20)+" Radio#:", radio, "Antenna#:", ant)
                if 1806799 < freq < 1816800:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b17.value(1) 
                    band='17'
                    print(band+" meters band, MCU:",str(b17)+" Radio#:", radio, "Antenna#:", ant)
                if 2099999 < freq < 2145000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b15.value(1) 
                    band='15'
                    print(band+" meters band, MCU:",str(b15)+" Radio#:", radio, "Antenna#:", ant)
                if 2489000 < freq < 2499000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b12.value(1) 
                    band='12'
                    print(band+" meters band, MCU:",str(b12)+" Radio#:", radio, "Antenna#:", ant)
                if 2696500<freq<2740500:
                    band='C.B. Band'
                if 2799999 < freq < 2970000:  
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b10.value(1)
                    band='10'
                    print(band+" meters band, MCU:",str(b10)+" Radio#:", radio, "Antenna#:", ant)
                if 4999999 < freq < 5400000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b6.value(1) 
                    band='6'
                    print(band+" meters band, MCU:",str(b6)+" Radio#:", radio, "Antenna#:", ant)
                if 14399999 < freq < 14800000:         
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b2.value(1)
                    band='2'
                    print(band+" meters band, MCU:",str(b2)+" Radio#:", radio, "Antenna#:", ant)
                if 42000000 < freq < 45000000:
                    b160.value(0),b80.value(0),b40.value(0),b30.value(0),b20.value(0),b17.value(0),\
                    b15.value(0),b12.value(0),b10.value(0),b6.value(0),b2.value(0),b70.value(0)
                    b70.value(1) 
                    band='70c'
                    print(band+" meters band, MCU:",str(b70)+" Radio#:", radio, "Antenna#:", ant)
                #Display outside the ham bands
                if 3000<freq<27900:
                    band='LongWave  '
                if 27999<freq<150000:
                    band= 'MediumWave  '
                if 150000 <freq< 179999 or 200001 <freq< 349999 or 400001 <freq< 533049 \
                    or 540351 <freq< 699999 or 730001 <freq< 1009999 or 1015001 <freq< 1400000 \
                     or 1435001 <freq< 1806800 or 1816800 <freq< 2100000 or 2145000 <freq< 2489000 \
                      or 2499000 <freq <2696500 or 2740500 <freq< 2800000 or 2970001 <freq< 3000000:
                    band= 'ShortWave  '
                if 3000001 <freq< 4999999 or 5400001 <freq< 14400000:
                    band='VHF       '
                if freq>30000000:
                    band='UHF       '
                
           
                if ant==2:
                    #Position 1
                    AnT='LONG WIRE'
                    Pin2.on()
                    sleep(0.1)
                    Pin4.on()
                    sleep(0.1)
                    Pin5.on()
                    
                if ant==0:
                    #Position 2
                    AnT='BEAM'
                    Pin2.off()
                    sleep(0.1)
                    Pin4.off()
                    sleep(0.1)
                    Pin5.on()
                    
                if ant==1:
                    #Position 3
                    AnT='40m DIPOLE'
                    Pin2.off()
                    sleep(0.1)
                    Pin4.on()
                    sleep(0.1)
                    Pin5.on()
                    
                if ant==3:
                    #Position 4
                    AnT='DUMMY LOAD'
                    Pin2.off()
                    sleep(0.1)
                    Pin4.off()
                    sleep(0.1)
                    Pin5.off()
                    
                    
                # OLED initialization for boot time information
                i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
                oled.fill(0)       
                oled.text('Band: ' + str(band) +' mtrs', 0,0)    
                oled.text('Ant: '+AnT, 0,20,1)         
                #Uncoment the line below if you want more information in auto mode
                #Make sure you coment out the RSSI line 230, 231
                #Frequency information on the OLED, too crowded for me
                #oled.text('Frq: '+ str(freq), 0, 10)    
                oled.show()
    except OSError:
        print('Error')
        oled.fill(0)
        oled.text('N1MM server down',1,1,1)
        oled.text('...rebooting',0,20,1)
        oled.show()
        sleep(1)
        autoAntenna()
        #machine.reset()

# This is the whole program, four lines of code, the rest is just fluff...HI                      
if 0==p36.value() or 0==p39.value() or 0==p34.value() or 0==p35.value():
    manualAntenna()
else:
    autoAntenna()         
