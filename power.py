# test simple gpio outputs
# will be for controlling power supplies eventually
# uses pin A5 (gps) and A6 (satcoms)

import pyb
import utime
from machine import Pin


class GPSpower:
	def __init__(self):
		self.pinA5 = pyb.Pin('A5',Pin.OUT)
	def power(self,s):
		self.pinA5.value(s)

def testgpio():
	led = pyb.LED(2)
	# create output on pin
	io1 = pyb.Pin('A5',Pin.OUT)
	for x in range(0,50):
		io1.value(1)
		pyb.delay(500)
		io1.value(0)
		pyb.delay(500)
		led.toggle()

def testgpio2():
	gpsp = GPSpower()
	for x in range(0,10):
		gpsp.power(1)
		pyb.delay(500)
		gpsp.power(0)
		pyb.delay(500)

testgpio2()

