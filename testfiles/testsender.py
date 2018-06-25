#!/usr/bin/env python
# test a transceiver - send some data and read it when it comes back
#import select
import pyb
import utime
from machine import Pin

# normal sleep - not very low power
redled = pyb.LED(1)
greenled = pyb.LED(2)

packet="1234567890"
ser = pyb.UART(1,9600)
ser.init(9600,bits=8,parity=None,timeout=2)

print("started sending")
while 1:
	ser.write(packet)
	# wait for something coming into our serial
	#while select.select(ser,[],[],0)

	data = ser.read()
	if data == packet :
		print("ok")
		greenled.on()
		utime.sleep_ms(300)
		greenled.off()
	else :
		print("x")
		redled.on()
		utime.sleep_ms(300)
		redled.off()
