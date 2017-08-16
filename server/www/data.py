import sys
sys.path.append("/home/glacsweb/picogps/server")

import gpsdb
from csvconvert import csv_convert

CONFIG = "/home/glacsweb/picogps/server/db.ini"

def index(req):
    output = ""
    req.content_type = "text/csv"
    DB = gpsdb.GpsDb(CONFIG)
    output += "Glacier,IMEI,timestamp,longitude,latitude,quality,hdop,sats\r\n"
    output += csv_convert(DB.get_data())
    return output
