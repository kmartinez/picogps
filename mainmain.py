#
# main picoGPS code

from ds3231 import DS3231
from gps import *
from sat import *
from common import d

schedule = [0 3 6 9 11 12 15 18 21]
transmit = [11]

#Get the current time
extrtc = DS3231()
(YY, MM, DD, hh, mm, ss, wday n1, n2) = extrtc.get_time()

if(hh in schedule and mm<10 and hh in transmit):
	#Satellite transmission time.
	satloop()

elif (hh in schedule and mm<10 and hh not in transmit):
	#GPS reading time
	gpsloop()
else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	sleep(10)



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

	while t<positiontimeout:
		start = millis()
		nmea = gpsuart.readline()
		thetype, data = processGPS(nmea)

		if(thetype=='t'):
			#We got a timestamp
			d('We got a timestamp')
			(gpsYY, gpsMM, gpsDD, gpshh, gpsmm, gpsss, gpswday gpsn1, gpsn2) = data

			# if gpstime is > 10s different from extrtc - set extrtc
			if(abs(gpsYY-YY)>0 or abs(gpsMM-MM)>0 or abs(gpsDD-DD)>0 or abs(gpshh-hh)>0 or abs(gpsmm-mm)>0 or abs(gpsss-ss)>10):
				#We should update the external RTC. We're greater than 10 seconds out.
				d('Setting external RTC. Theres a time difference.')
				extrtc.set_time(gpsYY, gpsMM, gpsDD, gpshh, gpsmm, gpsss)

		elif(thetype=='p'):
			#We got some positional data
			d('We got positional data')

			(lat,lon,alt,qual,hdop,sats) = data

			if(qual>=4):
				#We are happy with the quality of the GPS fix.
				finalgps = data
				gps10.append([lat,lon])

		else:
			#Theres been some kind of problem. Timeout?
			d('No data received - Timeout?')
			pass


		#Only store last 10 gps readings in array
		if(gps10.length>10):
			gps10.pop(0)

		foreach()


		#Set the time for our positiontimeout
		t = millis()-start

	# turn GPS off
	GPSpower.value(0)
