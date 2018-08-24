#
# main picoGPS code for glacsweb.org BergProbe
# check hour, do a job, set next alarm
# gps loop reads until it gets lots of fixes, saves last to data.txt
# sat loop Iridium sends fixes from file
# temperature included from am ADC
# K.Martinez and J.Curry, University of Southampton, 2017/8

import math
from time import sleep
from ds3231 import DS3231
from gps import *
from sat import *
from common import *
import stm

# What hours to do gps (must incl transmit)
schedule = [0,3,6,9,12,13,15,18,21]
# when to send data
transmit = [13]
# max time of gps loops in ms
positiontimeout = 200*1000
# use fix type of this quality (FIX 4)
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


def sendtosat():
	#Pull data from file and send it.
	data = []
	payload = ""
	i = 0

	#Get x readings from file.
	with open('data.txt','r') as file:
		for line in file:
			# need to swap \n for ; for iridium
				linenoCR = line.rstrip('\n')
				linenoCR = linenoCR + ';'
				payload = payload + linenoCR
				#only sending a few readings 300/50=6 max
				i = i + 1
				if(i >= 5):
					break
	d(payload)

	#We've finished all the readings
	if(len(payload)<10):
		#Empty payload
		return False

	# send fix via sat
	d('Sending fixes via Iridium')
	if sendmsg(payload) == True:
		d('Done')
		#Remove lines from file that we sent.
		file= open('data.txt','r')
		count = i
		# read the lines we sent
		while( count > 0):
			file.readline()
			count -= 1
		restoffile = file.read()
		file.close()
		file = open('data.txt','w')
		file.write(restoffile)
		file.close()
		return True

	else:
		d('SatSend failed')
		return False

# power up Iridium, wait for connection, send data file messages
def satloop():
	d('SAT on')
	satpower.value(1)
	#wait for sat to boot
	waitforsat()
	d('Getting Iridium signal')
	strength = satsignal()
	if (strength != None) and (int(strength) >= MINIRIDIUM) :
		d('OK Sat strength')
	else:
		d('Sat strength failed')
		satpower.value(0)
		return

	while(sendtosat()==True):
		d("Satellite data send complete.")

	#turn SAT off
	satpower.value(0)
	#we're done.
	return


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

	#turn GPS on
	gpspower.value(1)

	t = 0
	gps10 = []
	# wait for typ warm-up time
	d('waiting for warmup period')
	if(not waiter):
		sleep(11)
	d('starting gps loop')

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

		elif(thetype=='p'):
			#We got some positional data, may need to say q=4 ?
			(lat,lon,alt,qual,hdop,sats,nmeafix) = data
			print('Quality: ', qual)
			if(qual == FIXQUALITY):
				#count happy GPS fix.
				d('got fix')
				fixcount += 1

		else:
			#Theres been some kind of problem. Timeout?
			#d('No data received - Timeout?')
			pass

		# once we have seen 15 fixes we store and exit
		# At this point we assume we got a GPS datetime
		print('fixcount is ', fixcount)
		if(fixcount >= 15):
			# store it in file
			with open('data.txt','a') as file:
				# assume we saw timedate
				tostore = gpsYY[2:] + gpsMM + gpsDD + gpshh + gpsmm + "," + nmeafix + "," + temperature() + "\n"
				file.write(tostore)
			break


		# how long have we been looping? for positiontimeout
		t = pyb.millis()-start

	# turn GPS off
	d('GPS off')
	gpspower.value(0)


# debug gps stream print for tests
def printgps():
	while True:
		s = gpsuart.readline()
		if( s != None) :
			print(s)

# debug - print ext rtc date
def date():
	extrtc = DS3231()
	print(extrtc.get_time())
	
def standby():
	pyb.standby()

# dumper to get readings off Pico
def dumpfile():
	print('Start your log/capture - 10s to go')
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

def temperature():
	a = pyb.ADC(pyb.Pin.board.A5)
	g = pyb.Pin('A7', pyb.Pin.OUT_PP)
	g.high()
	sum = 0.0
	for count in range(1,100):
		w = a.read() * 3300 / 4096.0
		tc = ((10.888 - math.sqrt(118.548544 + 0.01388 * (1777.3 - w)))/-0.00694) + 30
		sum = sum + tc
	g.low()
	# we return C X 10 to save the decimal place
	temp = round(sum/100.0,1)
	# if its broken we will get out of range return 0
	if temp > 80 : return("0")
	return(str(int(temp * 10)))

def saton():
	satpower.value(1)
def satoff():
	satpower.value(0)
def gpson():
	gpspower.value(1)

def gpsoff():
	gpspower.value(0)

#Main run method. Run on startup.

#check the time.

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


if(hh in schedule and mm<10 and hh in transmit):
	#Time to send readings
	satloop()
	pyb.standby()

elif (hh in schedule and mm<10 and hh not in transmit):
	#GPS reading time
	gpsloop()
	pyb.standby()
else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	print('Press CTRL-C Now to prevent going back to sleep!')
	sleep(20)
	gpsoff()
	satoff()
	pyb.standby()

