# GPS functions
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
sample = "1701081400,5056.16376,123.74144,W,64.0,4,1.06,6"

def nmealon2lon( l):
	# convert text NMEA lon to degrees.decimalplaces
	degrees = float(l[0:3])
	decimals = float(l[3:])/60
	lon = degrees + decimals
	if f[3] == 'W':
		lon = -lon
	return(lon)

def nmealat2lat( nl):
	# convert text NMEA lat to degrees.decimalplaces
	degrees = float(nl[0:2])
	decimals = float(nl[2:])/60.0
	return(degrees + decimals)

def parsefixdata(data):
	f =  data.split(',')			
	datetime = f[1]
	lat = float(f[2][0:2]) + float(f[2][3:])/60.0
	lon = f[3]
	E = f[4]
	alt = f[5]
	qual = f[6]
	hdop = f[7]		
	sats = f[8]
	#location = (nmealat2lat(lat),nmealon2lon(lon), alt, qual,hdop,sats,nmeafix )
	return 'p', location
