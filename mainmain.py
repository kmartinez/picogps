#
# main picoGPS code

from ds3231 import DS3231
from gps import *
from sat import *
from common import d

#Setup debugging

disableDebug()

#Disable actually sending iridium messages (because $$$)
dryrun = 1

# just been woken up by alarm
# check we are on a scheduled hour
schedule = (0, 3, 6, 9, 12, 15, 18, 21)

#Get the current time
extrtc = DS3231()
(YY, MM, DD, hh, mm, ss, wday n1, n2) = extrtc.get_time()

if(hh in schedule and mm<10):
	#We're on schedule. Run the code as normal.
	main()
else:
	# if not we're in maintenance mode exit()
	enableDebug()
	d("Woken not on-schedule. Debug mode activated.")
	exit()


#Setup Globals

finalgps = ''

def main():
	d("We're on schedule. ")

	# turn on GPS
	GPSpower.value(1)

	# wait for GPS fix OR timeout - store

	while t<timeout:
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

			if(qual>=5):
				#We are happy with the quality of the GPS fix.
				finalgps = data
				break

		else:
			#Theres been some kind of problem. Timeout?
			d('No data received - Timeout?')
			pass

	# turn GPS off
	GPSpower.value(0)

	# turn SAT on
	SATpower.value(1)

	#wait for sat to boot
	waitforsat(satuart)

	strength = satsignal(satuart)
		if strength != None:
			d('Sat strength: ' + strength)

	# send fix via sat

	if(!dryrun) {
		d('Sending fix via satellite')
		sendmsg(satuart, ''.join(finalgps))
		d('Done interfacing with sat.')
	}

	SATpower.value(0)
	
	# turn SAT off

	# if not successful 
	#  store GPS fix in the file (check file is not at maxsize)

	# set next wakeup from schedule

	nexthour = -1

	for item in schedule:
		if(item>hh):
			nexthour = item
			break
	#We didnt find any next hour (roll around to beginning)
	if(nexthour==-1):
		nexthour = schedule[0]

	extrtc.setalarm(nexthour)

	d('END OF CODE')
	exit()

	#Need to be careful. If you wake it up and want it to go 
	#back into normal operation, need a function to set the RTC 
	#to the next available time and run again.

	# if we are not on USB:
	# deepsleep
	# pyb.stop()
