from gps import *
from sat import *
from time import sleep


while(1):
	dat = gpsuart.readline()
	(type, ret) = processGPS(dat)
	if(type=='p'):
		print(ret)
		(lat, lon, alt, a, b, c) = ret
		tosend = 'Hi. I am at ' + str(lat) + ', ' + str(lon) + ' Altitude: ' + str(alt)
		sendmsg(str(dat))
		print('Done sending')
		sleep(1)
		break
