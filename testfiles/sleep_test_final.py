#
# main picoGPS code
# Simplified test of immediate GPS read
# check hour, do a job, set next alarm
# gps job reads until it gets lots of fixes, saves to data.txt
# satjob sends batch of fixes from file

from ds3231 import DS3231
from gps import *
from sat import *
from common import *
import stm

schedule = [0,3,6,9,11,12,15,18,21]
transmit = [11]
# max number of loops in ms
positiontimeout = 60*1000
# use fix type of this quality (is FIX really 4?) HARDCODED NOW
FIXQUALITY = '4'
# minimum Iridium strength to use
MINIRIDIUM = 2
#Get the current time
print("AWAKE!")
extrtc = DS3231()

(YY, MM, DD, hh, mm, ss, wday, n1) = extrtc.get_time()
print(extrtc.get_time())

pin = pyb.Pin.board.A0                     
pin.init(mode = pyb.Pin.IN, pull = pyb.Pin.PULL_DOWN)
# In this mode pin has pulldown enabled
stm.mem32[stm.PWR + stm.PWR_CR] |= 4            # set CWUF to clear WUF in PWR_CSR
stm.mem32[stm.PWR + stm.PWR_CSR] |= 0x100       # Enable wakeup


extrtc.clearalarm()
extrtc.testalarm()
print("Waiting for sleep...")
print("type pyb.standby() to sleep (you have 20secs until wake)")