#!/usr/bin/env python3
# 26july - build whole data block
# assume everything is converted to floats
# sample data from 2018:
# date lat lon alt sats temp
# 1810100601,6400.7601232,1625.391151,93.70,16,-326;
import math
import struct
# conversion from our nmea format to real degrees
def nmealon2lon( l):
    # convert text NMEA lon to degrees.decimalplaces
    degrees = float(l[0:2])
    decimals = float(l[2:])/60
    lon = degrees + decimals
    # if f[3] == 'W':
    # 	lon = -lon
    return(lon)

def nmealat2lat( nl):
    # convert text NMEA lat to degrees.decimalplaces
    degrees = float(nl[0:2])
    decimals = float(nl[2:])/60.0
    return(degrees + decimals)

def deg2bin(deg):
    intpart = int(deg)
    frac = int(round(100000000.0 * (deg - intpart),0))
    # make the 4 byte array for this value
    decimals_ba = bytearray(frac.to_bytes(4, 'little'))

    # first byte deg  - with float part
    deg_ba = bytearray(intpart.to_bytes(1, 'little'))
    return deg_ba + decimals_ba

def alt2bin(alt):
    alt_cm = int(round(alt * 100.0,0))
    return bytearray(alt_cm.to_bytes(2, 'little'))

def temp2bin(t):
    '''(temperature offset to manage neg'''
    tr = int(round((t + 2560),0))
    return bytearray(tr.to_bytes(2, 'little'))

def sats2bin(sats):
    '''conv int sats to a byte'''
    return bytearray(sats.to_bytes(1, 'little'))


def timestamp2bin(timestamp_s):
    ''' convert from YYMMDDhhmm to YMDHm bytes'''
    print(timestamp_s)
    # should check if len == 10?
    # to_bytes different in modern python byteorder="little"
    Y = bytearray(int(timestamp_s[0:2]).to_bytes(1,"little"))
    M = bytearray(int(timestamp_s[2:4]).to_bytes(1,'little'))
    D = bytearray(int(timestamp_s[4:6]).to_bytes(1,'little'))
    H = bytearray(int(timestamp_s[6:8]).to_bytes(1,'little'))
    m = bytearray(int(timestamp_s[8:10]).to_bytes(1,'little'))
    return Y + M + D + H + m


def position2binary(reading):
    '''convert all string values to binary array'''
    e = reading.split(",")
    print(e)
    ts = e[0]
    lat = float(e[1])
    lon = float(e[2])
    alt = float(e[3])
    sats = int(e[4])
    temp = int(e[5])

    ts_ba = timestamp2bin(ts)
    lat_ba = deg2bin(lat)
    lon_ba = deg2bin(lon)
    alt_ba = alt2bin(alt)
    sats_ba = sats2bin(sats)
    temp_ba = temp2bin(temp)

    return ts_ba + lat_ba + lon_ba + alt_ba + sats_ba + temp_ba



print("binary version")
# 1810100601,6400.7601232,1625.391151,93.70,16,-326;
# we'll need to remove the ; between readings!
testreading = "1810100601,64.09371392,16.33418409,93.70,16,-326"
reading_bin = position2binary(testreading)
print(reading_bin)
print("%d bytes" % len(reading_bin))

#print(temp2bin(float("12.34")))
