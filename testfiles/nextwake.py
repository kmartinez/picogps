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

# set a test current hour
for hour in range(24):
	al = getnextalarm(hour)
	print('time=>alarm ',hour,'=>', al)
