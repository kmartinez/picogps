#!/usr/bin/env python
# test a radio transceiver using a Pico
# one mode repeats a transmission, the other receives it
#import select
import pyb
import utime
from machine import Pin
#mode = "BEEPER"
mode = "RECV"
redled = pyb.LED(1)
greenled = pyb.LED(2)

packetsOK = 0
packetsBAD = 0
# our test "packet" in binary so we could test 8 bit clear
packet=b'abcdefghijklmnopqrstuvwxyz1234567890'
ser = pyb.UART(1,38400)
ser.init(38400,bits=8,parity=None,timeout=2)

print("started")
if mode == "BEEPER" :
	while 1:
		greenled.on()
		ser.write(packet)
		utime.sleep_ms(1000)
		greenled.off()
if mode == "RECV" :
	while (ser.read(1) != b'0') :
		print("syncing")
	print("listening")
	try:
		while 1:
			data = ser.read()
			if data == None :
				continue
			# print(data)
			if data == packet :
				#print("ok")
				packetsOK += 1
				greenled.on()
				utime.sleep_ms(50)
				greenled.off()
			else :
				redled.on()
				packetsBAD += 1
				print(100 * packetsOK/(packetsOK + packetsBAD))
				utime.sleep_ms(50)
				redled.off()
	except KeyboardInterrupt:
		print(100 * packetsOK/(packetsOK + packetsBAD))
	
