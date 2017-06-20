from ds3231 import DS3231
from time import sleep
import utime, pyb

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