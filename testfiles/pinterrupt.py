# main.py 
# test wake on pin change

#import pyb (ALREADY IN BOOT.PY)
import utime
from machine import Pin


def testrtc():
	rtc = pyb.RTC()	
	rtc.datetime((2017,3,20,10,15,0,0,0))
	for x in range(0,10):	
		print(rtc.datetime() )
		utime.sleep_ms(1000)
		
def callback(line):
	print("line =", line)
	#for x in range(0,5):
	#	led.toggle()
	#	pyb.delay(200)
	#	led.toggle()
	#	pyb.delay(200)

def testalarm():
	# config wakeup every N ms
	rtc = pyb.RTC()
	rtc.wakeup(10000)
	

def setupwakepin():
	# config a GPIO to cause an interrupt
	extint = pyb.ExtInt('B5', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback)

print("checking if on USB")
# can use this to prevent deepsleep if on usb
if pyb.USB_VCP().isconnected():
	print ("we are on usb")

extint = pyb.ExtInt('B5', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback)
led = pyb.LED(1)
for x in range(0,50):
	led.toggle()
	pyb.delay(500)
	led.toggle()
	pyb.delay(500)
