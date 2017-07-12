#!/usr/bin/env python
#$GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
#1    = UTC of Position
#2    = Latitude
#3    = N or S
#4    = Longitude
#5    = E or W (negate if W)
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
# time date message (need enabling)
#import serial

def nmealon2lon( l):
	# convert text NMEA lon to degrees.decimalplaces
	degrees = float(l[0:3])
	decimals = float(l[3:11])/60
	lon = degrees + decimals
	if nmea[2] == 'W':
		lon = -lon
	return(lon)

def nmealat2lat( nl):
	# convert text NMEA lat to degrees.decimalplaces
	degrees = float(nl[0:2])
	decimals = float(nl[2:10])/60
	return(degrees + decimals)

#ser = serial.Serial('/dev/ttyUSB0',38400)
#file = open("log.txt","w")

ser = gpsuart

print("lat lon alt qual hdop sats")
while 1:
	data = ser.readline()
	#data = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
	
	if data.startswith( '$GPGGA' ) or data.startswith('$GNGGA') :
		f =  data.split(',')			
		gpstime = f[1].split(".")[0]
		lat = f[2]
		lon = f[4]
		E = f[5]
		qual = f[6]
		sats = f[7]		
		hdop = f[8]		
		alt = f[9]
		nmea = (lat, lon, E, alt, qual, hdop, gpstime, sats)
		#print format(nmea)
		# need to limit lat and lon to 10 decimal places? and compose string to save
		location = (nmealat2lat(lat),nmealon2lon(lon), alt, qual,hdop,sats )
		print(location)
		#file.write(format(nmea) + "\n")
			
	if data.startswith( '$GPZDA' ) or data.startswith('$GNZDA') :
		# $GPZDA,hhmmss.ss,dd,mm,yyyy,xx,yy*CC
		# ignore decimals seconds
		print(data)
		fields = data.split(",")
		hms = fields[1]
		tod = (hms[0:2], hms[2:4], hms[4:6], fields[2], fields[3], fields[4])		
		print(tod)
