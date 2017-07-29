#
# main picoGPS code
# Simplified test of immediate GPS read

from ds3231 import DS3231
from gps import *
from sat import *
from common import d
schedule = [0,3,6,9,11,12,15,18,21]
transmit = [11]
global finalgps
# max number of loops in ms
positiontimeout = 60*1000
# use fix type above this quality (garden was only 1 :-(
QUALTHRESH = 0 

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



def satloop():

	data = []
	payload = ""

	with open('data.txt','r') as file:
		i = 0
		for line in file:
			#Check we are only sending a few readings.
			i = i + 1
			if(i>8):
				break
			#Load readings into file
			line_Str=file.readline()
			line_Str=line_Str.rstrip('\n')
			line_Str=line_Str.rstrip('\r')
			data.append(line)

	for item in data:
		payload = payload + data

	# turn SAT on
	SATpower.value(1)
	#wait for sat to boot
	waitforsat(satuart)

	strength = satsignal(satuart)
	if strength != None:
		d('Sat strength: ' + strength)
	else:
		pass

	# send fix via sat

	d('Sending fix via satellite')
	sendmsg(satuart, ''.join(finalgps))
	d('Done interfacing with sat.')

	#turn SAT off
	SATpower.value(0)
	#we're done.
	return



def gpsloop():

	#turn GPS on
	GPSpower.value(1)

	t = 0
	gps10 = []
	# wait for typ warm-up time
	d('waiting for warmup period')
	sleep(1)
	d('starting gps loop')

	while t < positiontimeout:
		start = pyb.millis()
		nmea = gpsuart.readline()
		if nmea == None:
			break
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
			#We got some positional data
			d('got position')

			(lat,lon,alt,qual,hdop,sats) = data
			d(qual)
			if(int(qual) > QUALTHRESH):
				#We are happy with the quality of the GPS fix.
				finalgps = data
				d(finalgps)
				gps10.append([lat,lon])

		else:
			#Theres been some kind of problem. Timeout?
			d('No data received - Timeout?')
			pass

		#Only store last 10 gps readings in array
		if(len(gps10) > 10):
			# we will just terminate after ten
			for count in range(0,9):
				avlat += gps10[count][0]
				avlon += gps10[count][1]
			print( avlat/10, avlon/10) 
			break
			#gps10.pop(0)


		#Set the time for our positiontimeout
		t = pyb.millis()-start

	# turn GPS off
	#GPSpower.value(0)

gpsloop()
print(finalgps)
