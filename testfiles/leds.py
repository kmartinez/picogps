# main.py 
# test various led things

import pyb
import utime
from machine import Pin

# normal sleep - not very low power
def flash():
	redled = pyb.LED(1)
	greenled = pyb.LED(2)
	for x in range(0,10):
		redled.on()
		utime.sleep_ms(500)
		redled.off()
		utime.sleep_ms(500)
		greenled.on()
		utime.sleep_ms(500)
		greenled.off()
		utime.sleep_ms(500)

flash()

