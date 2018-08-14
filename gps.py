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
from common import d
def nmealon2lon( l):
	# convert text NMEA lon to degrees.decimalplaces
	degrees = float(l[0:3])
	decimals = float(l[3:])/60
	lon = degrees + decimals
	# if f[3] == 'W':
	# 	lon = -lon
	return(lon)

def nmealat2lat( nl):
	# convert text NMEA lat to degrees.decimalplaces
	degrees = float(nl[0:2])
	decimals = float(nl[2:])/60.0
	return(degrees + decimals)

f = None

def processGPS(data):
	if data.startswith( '$GPGGA' ) or data.startswith('$GNGGA') :
		#It's positional data
		data = str(data)
		# Why?
		global f
		f =  data.split(',')			
		gpstime = f[1].split(".")[0]
		lat = f[2]
		lon = f[4]
		E = f[5]
		qual = f[6]
		sats = f[7].lstrip("0")		
		hdop = str(int(round(float(f[8]),0) ) )		
		alt = f[9]
		nmeafix = lat + "," + lon.strip('0') + "," + alt + "," + sats 
		location = (nmealat2lat(lat),nmealon2lon(lon), alt, qual,hdop,sats,nmeafix )
		return 'p', location
			
	elif data.startswith( '$GPZDA' ) or data.startswith('$GNZDA') :
		# It's timing data
		# $GPZDA,hhmmss.ss,dd,mm,yyyy,xx,yy*CC
		# ignore decimals seconds, keep 20xx year for our rtc
		data = str(data)	
		fields = data.split(",")
		hms = fields[1]
		#	YYYY	MM	DD	hh 	mm	ss
		tod = (fields[4], fields[3], fields[2], hms[0:2], hms[2:4], hms[4:6])	
		return "t", tod

	else:
		#No known string detected == probably timeout
		return None, None
