# main.py -- put your code here!

import pyb
import utime
from machine import Pin
#import machine


print("starting standby test in 20s")
pyb.delay(20000)	
pyb.stop()
print("wokenup. yay")


# deep sleep - pyb.standby()

