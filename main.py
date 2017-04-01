# main.py -- put your code here!

import pyb
import utime
from machine import Pin
#import machine

# normal sleep - not very low power
def testsleep():
	led = pyb.LED(1)
	for x in range(0,10):
		led.toggle()
		utime.sleep_ms(2000)
		led.toggle()
		utime.sleep_ms(2000)

def testrtc():
	rtc = pyb.RTC()	
	rtc.datetime((2017,3,20,10,15,0,0,0))
	for x in range(0,10):	
		print(rtc.datetime() )
		utime.sleep_ms(1000)
		
def wokenup():
	print("wokenup")
	#for x in range(0,5):
	#	led.toggle()
	#	pyb.delay(200)
	#	led.toggle()
	#	pyb.delay(200)

def testalarm():
	# config wakeup every N ms
	rtc = pyb.RTC()
	rtc.wakeup(10000)
	
	
			

def testpin():
	# create input on pin
	led = pyb.LED(1)
	p5 = pyb.Pin('B5',Pin.IN, Pin.PULL_UP)
	for x in range(0,50):
		if p5.value() == 1 :
			led.on()
		else :
			led.off()

		pyb.delay(100)

print("starting  test in 1s")
pyb.delay(1000)	
testpin()
#pyb.stop()
# deep sleep - pyb.standby() danger!

