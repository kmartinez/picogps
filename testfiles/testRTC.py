from ds3231 import DS3231
from time import sleep
import utime, pyb

a = pyb.Pin('B3', pyb.Pin.IN, pyb.Pin.PULL_UP)
b = pyb.Pin('B10', pyb.Pin.IN, pyb.Pin.PULL_UP)


rtc = pyb.RTC()

extrtc = DS3231()


def printnow():
	print("ext rtc:")
	print ( extrtc.get_time() )

printnow()

extrtc.clearalarm()
extrtc.testalarm()

# for i in range(0,15):
# 	printnow()
# 	sleep(1)