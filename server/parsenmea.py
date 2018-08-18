# convert our nmea-like data to real coordinates

import datetime
#2017 format
#1    = YYMMDDHHmm
#2    = Latitude in nmea format
#3    = Longitude in nmea format
#4    = E or W (negate Longitude if W)
#5 = ALtitude above datum
#6    = GPS quality indicator 4 fix 5 float
#7    = Horizontal dilution of position
#8    = Number of satellites in use [not those in view]
sample2017 = '1707301731,6354.1234567,1638.1234567,130.71,5,1.4,8'

#2018 format
#0    = YYMMDDHHmm
#1    = Latitude in nmea format
#2    = Longitude in nmea format
#3 = ALtitude above datum
#4    = Number of satellites in use [not those in view]
#5 = temperature
sample2018 = '1707301731,6354.1234567,1638.1234567,130.71,8,215'


def parsefixdata(data):
    f = data.replace(";", "").split(',')
    timestamp = datetime.datetime.strptime(f[0], "%y%m%d%H%M")
    # only works if above 10 degrees!
    lat = float(f[1][0:2]) + (float(f[1][2:])/60.0)
    # carefully take one or two figures from lat as we stripped 00s
    decpart = f[2].split('.')[0] # 138
    fracpart = decpart[len(decpart)-2:] # 38
    #print(decpart)
    decpart = decpart[:len(decpart)-2]
    #print(decpart)
    fracpart = fracpart + '.' + f[2].split('.')[1] # 4868206
    #print(fracpart)
    lon = float(decpart) + (float(fracpart)/60.0)
    #E = f[3]
    #assume all West if f[3] == 'W':
    lon = -lon
    alt = float(f[3])
    if len(f) == 7: # old style message
        qual = int(f[4])
        hdop = float(f[5])
        sats = int(f[6])
        temperature = None
    else: # 2018 style message
        qual = None
        hdop = None
        sats = int(f[4])
        temperature = (float(f[5])/10)
    #0s are stripped off the data, it won't get a fix with just
    # 1 satelite so this must be a stripped character so change
    # it to 10 before going any further
    if sats == 1:
        sats = 10
    location = (timestamp, lat, lon, alt, qual, hdop, sats, temperature)
    return location


if __name__ == "__main__":
    loc = parsefixdata(sample2017)
    print(loc)
    loc2 = parsefixdata(sample2018)
    print(loc2)
