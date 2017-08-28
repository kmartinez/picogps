#
# repeat hourly say coms tests
# K.Martinez and J.Curry, University of Southampton, 2017

from ds3231 import DS3231
from sat import *
from common import *
import stm

# What hours to do gps (must incl transmit)
schedule = [0,3,6,9,12,13,14,15,16,17,18]
# when to send data
transmit = [13]
# max time of gps loops in ms
positiontimeout = 200*1000
# use fix type of this quality (dGPS FIX is 4)
FIXQUALITY = '4'
# minimum Iridium strength to use
MINIRIDIUM = 2
#Get the current time
extrtc = DS3231()

#Wakeup code run on startup is at bottom of file.


#get next alarm time

def getnextalarm(hh):
	nexttime = None

	if(hh in schedule):
		position = schedule.index(hh)
		nextpos = position+1
		if(nextpos>(len(schedule)-1)):
			nextpos = 0
		nexttime = schedule[nextpos]
	else:
		for i in schedule:
			if(i>hh):
				nexttime = i
				break
		if(nexttime==None):
			nexttime = 0
	return nexttime


# power up Iridium, wait for connection, send test message
def satloop():

	d('SAT on')
	satpower.value(1)
	#wait for sat to boot
	waitforsat()
	# need to check return from above!!!
	d('Getting Iridium signal')
	strength = satsignal()
	if (strength != None) and (int(strength) >= MINIRIDIUM) :
		d('OK Sat strength')
	else:
		d('Sat strength failed')
		satpower.value(0)
		return

	ti = extrtc.get_time()
	message = "testing at " + str(ti[3]) + str(ti[4])
	print(message)
	sendmsg(message)
	#turn SAT off
	satpower.value(0)
	#we're done.
	return



# debug gps stream print for tests
def printgps():
	while True:
		s = gpsuart.readline()
		print(s)

# debug - print ext rtc date
def date():
	extrtc = DS3231()
	print(extrtc.get_time())
	
def standby():
	pyb.standby()

# vital dumper in case of stuck readings on Pico
def dumpfile():
	# really need to sleep(10) so logging can be started
	print('Start logger - 10s to go')
	sleep(10)
	try:
		fd = open('data.txt','r')
		b = " "
		while b != "" :
				b = fd.readline()
				print(b)
		fd.close()
	except :
		d('no data file')

# useful with cold hands
def saton():
	satpower.value(1)

def satoff():
	satpower.value(0)
def gpson():
	gpspower.value(1)

def gpsoff():
	gpspower.value(0)

#Main run method. Run on startup.

#First check the time.

(YY, MM, DD, hh, mm, ss, wday, n1) = extrtc.get_time()
if YY == '1900' :
	print('You need to set extrtc')

#Setup wake interrupt
pin = pyb.Pin.board.A0                     
pin.init(mode = pyb.Pin.IN, pull = pyb.Pin.PULL_DOWN)
# In this mode pin has pulldown enabled
stm.mem32[stm.PWR + stm.PWR_CR] |= 4            # set CWUF to clear WUF in PWR_CSR
stm.mem32[stm.PWR + stm.PWR_CSR] |= 0x100       # Enable wakeup

#Set next alarm time
extrtc.clearalarm()
nextwake = getnextalarm(hh)
extrtc.setalarm(nextwake)
print('\nWAKEUP', str(hh)+":"+str(mm), '=> **', nextwake, "hrs **. ALARM SET\n")


if(hh in schedule and mm<10 ):
	#Time to test
	satloop()
	pyb.standby()

else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	print('Press CTRL-C Now to prevent going back to sleep!')
	sleep(20)
	pyb.standby()

