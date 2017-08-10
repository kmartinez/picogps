#
# main picoGPS code for Base stations
# Simplified test of immediate GPS read

from ds3231 import DS3231
from gps import *
from sat import *
from common import d
schedule = [0,3,6,9,11,12,15,18,21]
transmit = [11]
# max number of loops in ms
positiontimeout = 60*1000
# use fix type above this quality (is FIX really 4?)
QUALTHRESH = 3 

#Get the current time
#extrtc = DS3231()
#(YY, MM, DD, hh, mm, ss, wday, n1, n2) = extrtc.get_time()

#if(hh in schedule and mm<10 and hh in transmit):
	#satloop()

#elif (hh in schedule and mm<10 and hh not in transmit):
	##GPS reading time
	#gpsloop()
#else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	#sleep(10)

# vital dumper in case of stuck readings on Pico
def dumpfile():
	# really need to sleep(10) so logging can be started
	fd = open('data.txt','r')
	b = " "
	while b != "" :
		b = fd.readline()
		print(b)
	
# could just check time messages ONCE
def gpsloop():
	global finalgps
	fixcount = 0
	#turn GPS on
	GPSpower.value(1)

	t = 0
	gps10 = []
	# wait for typ warm-up time
	d('waiting for warmup period')
	sleep(11)
	d('starting gps loop')

	while t < positiontimeout:
		start = pyb.millis()
		nmea = gpsuart.readline()
		if (nmea == None) or (len(nmea) < 32):
			continue
		thetype, data = processGPS(nmea)

		if(thetype=='t'):
			#We got a timestamp
			d('got timestamp')
			(gpsYY, gpsMM, gpsDD, gpshh, gpsmm, gpsss ) = data

			# if gpstime is > 10s different from extrtc - set extrtc
			#BROKEN RTC if(abs(gpsYY-YY)>0 or abs(gpsMM-MM)>0 or abs(gpsDD-DD)>0 or abs(gpshh-hh)>0 or abs(gpsmm-mm)>0 or abs(gpsss-ss)>10):
				#update external RTC. We're >10s out
				#d('Setting ext RTC')
				#extrtc.set_time(gpsYY, gpsMM, gpsDD, gpshh, gpsmm, gpsss)

		elif(thetype=='p'):
			#We got some positional data, may need to say q=4 ?
			d('got position')
			(lat,lon,alt,qual,hdop,sats,nmeafix) = data
			if(int(qual) > QUALTHRESH):
				#count happy GPS fix.
				fixcount += 1

		else:
			#Theres been some kind of problem. Timeout?
			#d('No data received - Timeout?')
			pass

		#once we have seen 15 fixes we store and exit QUICKHACK
		if(fixcount >= 15):
			# store it in file
			with open('data.txt','a') as file:
				# assume we saw timedate for now
				tostore = gpsYY[2:] + gpsMM + gpsDD + gpshh + gpsmm + "," + nmeafix
				file.write(tostore)
			break


		#Set the time for our positiontimeout
		t = pyb.millis()-start

	# turn GPS off
	d('GPS off')
	GPSpower.value(0)
# for now ignore time etc from GPS - will need wake-up check code though
GPSpower.value(1)
