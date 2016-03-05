#!/usr/bin/python
__author__="f0xd3v1lsw1ld@gmail.com"

import sys, time, smbus
#define used iic bus of rpi
iic_bus = 1
#define chip addrss, get with i2cdetect -y 1
iic_addr = 0x50
#EErom register
reg=0x00
#return value
ret=[]
#init smbus
eeprom = smbus.SMBus(iic_bus)

start=0x18
#data="www.raspberrypi.org"
data = [0x77,0x77,0x77,0x2e,0x72,0x61,0x73,0x70,0x62,0x65,0x72,0x72,0x70,0x69,0x2e,0x6f,0x72,0x67]
data1 =0x08
data2=[0x00, 0x13, 0xA0]

print("Try to write to eeprom 0x%02X" % iic_addr)

try:
 #first loop for url
 for i in range(len(data)):
   eeprom.write_byte_data(iic_addr,start+i,data[i])
   time.sleep(0.1)

 eeprom.write_byte_data(iic_addr,start+len(data),data1)
 time.sleep(0.1)

 start = 0x31  #start+len(data)+1
 #second loop
 for i in range(len(data)):
   eeprom.write_byte_data(iic_addr,start+i,data[i])
   time.sleep(0.1)

 start = start+len(data)

 for i in range(len(data2)):
   eeprom.write_byte_data(iic_addr,start+i,data2[i])
   time.sleep(0.1)

except IOError, err:
  print("Error during communication with Device: 0x%02X" % iic_addr)
  exit(-1)
time.sleep(0.1)

for i in range(0,255):
 try:
  ret.append(eeprom.read_byte_data(iic_addr, reg+i))
 except IOError, err:
  print("Error during communication with Device: 0x%02X" % iic_addr)
  exit(-1)

print(ret)
out=""
for item in ret:
 out+="%c"%item

print(out)

