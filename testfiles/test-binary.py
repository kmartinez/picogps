#!/usr/bin/env python3

import math
import struct
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

b = bytearray(5)
latnmea = "6405.6228352"
# actual value in degrees
latrealtext = "64.09371392"


#print( longdeg, longfrac)
#b[0] = longdeg
#print(longfrac | 0xff)
#b[1] = longfrac | 0xff
#print(b[0])
#print(b[1])

latf = nmealat2lat(latnmea)

latf = 64.12345678
print("starting with an easy lat valkue %f",latf)
#print("float value %.8f" % latf)
#fraction, decimals = math.modf(latf)
#print(int(decimals), fraction)
# take int part for degrees, subtract it to get frac part
intpart = int(latf)
frac = latf - intpart
print("fraction %.8f" % frac)
fracs = int(100000000 * frac)
print("scaled up fraction %d" % fracs)


#make the 4 byte array for this value
#baf = bytearray(struct.pack('i',fracs))
baf = bytearray(fracs.to_bytes(4,byteorder='big'))
print(baf)
#print("length ", len(baf))
#get the first byte - for the degrees
bai = bytearray(intpart.to_bytes(1,byteorder='big'))
print("bai ",bai)
latbytes = bai + baf
print(latbytes)
print("frac from bytes %d" % int.from_bytes(baf,"big",signed=False))
print("recovering value")
bai2 = latbytes[0]

print("degrees %d" % bai2)
print(latbytes[1:5])
print("degrees frac %d" % int.from_bytes(latbytes[1:5],"big"))