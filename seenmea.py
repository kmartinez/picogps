#!/usr/bin/env python
#$GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
#1    = UTC of Position
#2    = Latitude
#3    = N or S
#4    = Longitude
#5    = E or W
#6    = GPS quality indicator (0=invalid; 1=GPS fix; 2=Diff. GPS fix)
#7    = Number of satellites in use [not those in view]
#8    = Horizontal dilution of position
#9    = Antenna altitude above/below mean sea level (geoid)
#10   = Meters  (Antenna height unit)
#11   = Geoidal separation (Diff. between WGS-84 earth ellipsoid and
#       mean sea level.  -=geoid is below WGS-84 ellipsoid)
#12   = Meters  (Units of geoidal separation)
#13   = Age in seconds since last update from diff. reference station
#14   = Diff. reference station ID#
#15   = Checksum
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
file = open("log.txt","w")
print("lat lon alt qual hdop time sats")
while 1:
	data = ser.readline()
	
	if data.startswith( '$GPGGA' ) or data.startswith('$GNGGA') :
		f =  data.split(',')			
		gpstime = f[1].split(".")[0]
		lat = f[2]
		lon = f[4]
		qual = f[6]
		sats = f[7]		
		hdop = f[8]		
		alt = f[9]
		nmea = (lat, lon, alt, qual, hdop, gpstime, sats)
		print format(nmea)
		file.write(format(nmea) + "\n")
			
			
