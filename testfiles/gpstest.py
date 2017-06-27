from gps import *

while(1):
	dat = gpsuart.readline()
	print(str(dat))
	print(processGPS(dat))
