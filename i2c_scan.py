# Scanner i2c en MicroPython | MicroPython i2c scanner
# Renvoi l'adresse en decimal et hexa de chaque device connecte sur le bus i2c
# Return decimal and hexa adress of each i2c device
# https://projetsdiy.fr - https://diyprojects.io (dec. 2017)

import machine
from machine import Pin, SoftI2C
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=200000)
#i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hex address: ",hex(device))