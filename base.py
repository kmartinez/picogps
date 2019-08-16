#
# main picoGPS code for a BASE STATION
# Simplified test of immediate GPS read
# check hour, do a job, set next alarm
# gps job reads until it gets lots of fixes, saves to data.txt
# satjob sends batch of fixes from file
from time import sleep
from ds3231 import DS3231
from gps import *
#from sat import *
from common import *
import stm

# real one
# copy of rover schedule = [0,3,6,9,11,12,15,18,21]
schedule = [0,3,6,9,12,15,18,21]
# to delete! transmit = [22]
# max number of loops in ms
positiontimeout = 10*1000

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


def gpsloop(waiter=False):
	global finalgps
	fixcount = 0
	CheckedRTC = False
	gpsYY = ''
	gpsMM = ''
	gpsDD = ''
	gpshh = ''
	gpsmm = ''
	nmeafix = ''

	t = 0
	gps10 = []
	# wait for typ warm-up time
	d('waiting for warmup period')
	if(not waiter):
		sleep(11)
	d('starting gps loop waiting for datetime')

	start = pyb.millis()
	while t < positiontimeout:
		thetype = ''
		nmea = gpsuart.readline()
		if (nmea == None) or (len(nmea) < 32):
			continue
		try:
			thetype, data = processGPS(nmea)
		except:
			d('processGPS ERROR - continuing.')

		if(thetype=='t'):
			#We got a timestamp
			d('got timestamp')
			fixcount = 1
			(gpsYY, gpsMM, gpsDD, gpshh, gpsmm, gpsss ) = data
			if CheckedRTC != True:
				CheckedRTC = True
				# get our current datetime from rtc
				(YY, MM, DD, hh, mm, ss, wday, n1) = extrtc.get_time()
				# if gpstime is > 10s different from extrtc - set extrtc
				if(abs(int(gpsYY)-YY)>0 or abs(int(gpsMM)-MM)>0 or abs(int(gpsDD)-DD)>0 or abs(int(gpshh)-hh)>0 or abs(int(gpsmm)-mm)>0 or abs(int(gpsss)-ss)>10):
					#update external RTC. We're >10s out
					d('Setting ext RTC')
					# what to set for wday? 0 ?
					extrtc.set_time(int(gpsYY), int(gpsMM), int(gpsDD), 0, int(gpshh), int(gpsmm), int(gpsss))
					

		else:
			#Theres been some kind of problem. Timeout?
			#d('No data received - Timeout?')
			pass

		#once we have seen one we carry on
		# At this point we assume we got a GPS timestamp
		print('timestamp count ', fixcount)
		if(fixcount >= 0):
			break


		#Set the time for our positiontimeout
		t = pyb.millis()-start


# useful with cold hands
def setrtc(YY,MM,DD,hh,mm,ss):
        print('make sure you used UTC')
        extrtc.set_time(int(YY), int(MM), int(DD), 0, int(hh), int(mm), int(ss))
        date()

def gpson():
	gpspower.value(1)

def gpsoff():
	gpspower.value(0)

# debug gps stream print for tests
def printgps():
	while True:
		s = gpsuart.readline()
		print(s)

# debug - print ext rtc date
def date():
	print(extrtc.get_time())
	
def standby():
	pyb.standby()

# vital dumper in case of stuck readings on Pico
def dumpfile():
	# really need to sleep(10) so logging can be started
	print('Start logger - 10s to go')
	sleep(1)
	try:
		fd = open('data.txt','r')
		b = " "
		while b != "" :
				b = fd.readline()
				print(b)
		fd.close()
	except :
		d('no data file')


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

if (hh in schedule and mm<10):
	#turn ON GPS
	gpson()
        sleep(15)
	# wait for a GPS datetime
	gpsloop()
	# critical overlap time with rover and sets our energy use
        print("Keeping GPS on to broadcast")
	sleep(180)
	# turn GPS off
	gpsoff()
	d('GPS off')
	pyb.standby()
else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	print('Press CTRL-C Now to prevent going back to sleep!')
	sleep(20)
	pyb.standby()


# These are just for our non scheduled tests! REMOVE


# gpsloop()
# satloop()
