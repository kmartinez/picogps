#
# Set next wakeup alarm

#from ds3231 import DS3231
#from common import *
schedule = [0,3,6,9,11,12,15,18,21]
transmit = [11]
#Get the current time
#extrtc = DS3231()
#(YY, MM, DD, hh, mm, ss, wday, n1) = extrtc.get_time()
#if(hh in schedule and mm<10 and hh in transmit):
	#satloop()
	#Set Next Wakeup

#elif (hh in schedule and mm<10 and hh not in transmit):
	##GPS reading time
	#gpsloop()
	#Set Next Wakeup
#else:
	#We've been woken up externally. Wait for CTRL-C or sleep.
	#sleep(10)

# using current hour hh work out what the next hour is for alarm
def setnextalarm():
	lastone = len(schedule)-1
	for h in range(len(schedule)):
		if schedule[h] == hh:
			if h == lastone:
				# set alarm
				# extrtc.set_alarm(schedule[0])
				return(schedule[0])
			# set alarm
			# extrtc.set_alarm(schedule[h+1])
			return(schedule[h+1])
	# if we get here we need to find next closest alarm
	# FAILS at the moment
	if hh > 21:
		# set alarm to 0
		return(0)
	for h in range(len(schedule)-1):
		print('checking against ',schedule[h])
		if schedule[h] > hh:
			if h == lastone-1:
				# alarm should be first one 0
				print('alarm set to 0')
				return(0)
			else:
				# set alarm to next one
				return( schedule[h+1])
		
# set a test current hour
for hh in range(23):
	print('time now',hh)
	al = setnextalarm()
	print('next alarm set to',al)
