from mod_python import util 
import sys
sys.path.append("/home/glacsweb/picogps/server")

import gpsdb
from csvconvert import csv_convert
from processdata import add_dist_vel
CONFIG = "/home/glacsweb/picogps/server/db.ini"

def index(req):
    output = ""
    DB = gpsdb.GpsDb(CONFIG)
    parameters = util.FieldStorage(req, keep_blank_values=1)
    if not "imei" in parameters.keys():
        output += "Glacier,IMEI,timestamp,longitude,latitude,altitude,quality,hdop,sats,temperature\r\n"
        output += csv_convert(DB.get_data())
    else:
        output += csv_convert(
            add_dist_vel(DB.get_data_imei(parameters.getfirst("imei"))))
    req.content_type = 'text/csvi'
    req.headers_out.add("Content-Disposition", "attachment;filename=tracker.csv")

    return output
