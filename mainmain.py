#
# main picoGPS code

<<<<<<< HEAD
from ds3231 import DS3231
from gps import processGPS
from common import d

#Setup debugging

disableDebug()

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

	# send fix via sat
	
	
	# turn SAT off

	# if not successful 
	#  store GPS fix in the file (check file is not at maxsize)

	# set next wakeup from schedule

	# if we are not on USB:
	# deepsleep
	# pyb.stop()
=======
# just been woken up by alarm

# check we are on a scheduled hour
schedule = (0, 3, 6, 9, 12, 15, 18,21)

# if not we're in maintenance mode exit()

# turn on GPS
# wait for GPS fix OR timeout - store
# turn GPS off

# if gpstime is > 10s different from extrtc - set extrtc

# turn SAT on
# send fix via sat
# turn SAT off

# if not successful 
#  store GPS fix in the file (check file is not at maxsize)

# set next wakeup from schedule

# if we are not on USB:
# deepsleep
# pyb.stop()
>>>>>>> a01b07af3e16f7a272c3f8844f40036008d33878
