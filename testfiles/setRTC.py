from ds3231 import DS3231

import utime, pyb

rtc = pyb.RTC()

extrtc = DS3231()

def printnow():
	print("ext rtc:")
	print ( extrtc.get_time() )

printnow()
