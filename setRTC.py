from ds3231_pb import DS3231

import utime, pyb

rtc = pyb.RTC()

extrtc = DS3231("y")

def now():
	print("ext rtc:")
	print ( extrtc.get_time() )


