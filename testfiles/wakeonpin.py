# main.py 
# test wake on pin change

#import pyb (ALREADY IN BOOT.PY)
import utime, upower, machine
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

# can use this to prevent deepsleep if on usb

#extint = pyb.ExtInt('A0', pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback)
# simmulate a job
led = pyb.LED(1)
wkup = upower.wakeup_X1()
for x in range(0,50):
	led.on()
	pyb.delay(50)
	led.off()
	pyb.delay(450)
	
if pyb.USB_VCP().isconnected():
	print ("we are on usb")
	led.on()
else:		
	wkup.enable()
	pyb.standby()
