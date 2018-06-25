import sys
sys.path.append("/home/glacsweb/picogps/server")

import gpsdb
import datetime 
from csvconvert import csv_convert

CONFIG = "/home/glacsweb/picogps/server/db.ini"

def index(req):
    output = "<html><head><title>Glacier Tracker Status</title></head><body>"
    output += "<h1>Glacier Tracker Status</h1>\r\n"
    output += "<h2>Latest Data Summary</h2>\r\n"
    output += ("<p>As at %s UTC</p>" % datetime.datetime.utcnow())
    output += ("<table  border><tr><th>Glacier</th><th>IMEI</th><th>Timestamp</th>" + 
        "<th>Longitude</th><th>Latitude</th><th>Altitude</th><th>Quality</th>" +
        "<th>HDOP</th><th>Satellites</th><th>Position Count</th><th>View</th></tr>")
    DB = gpsdb.GpsDb(CONFIG)
    LATEST = DB.get_latest_data()
    for SITE in LATEST:
        COUNT = DB.get_data_count(SITE[1])
        output += "<tr>"
        output += ("<td>%s</td>" % SITE[0])
        output += (
            "<td><a href = \"data.py?imei=%s\">%s</a></td>" % 
            (SITE[1], SITE[1]))
        output += ("<td>%s</td>" % SITE[2])
        output += ("<td>%s</td>" % SITE[3])
        output += ("<td>%s</td>" % SITE[4])
        output += ("<td>%s</td>" % SITE[5])
        output += ("<td>%s</td>" % SITE[6])
        output += ("<td>%s</td>" % SITE[7])
        output += ("<td>%s</td>" % SITE[8])
        output += ("<td>%s</td>" % COUNT)
        output += ("<td>")
        output += ("<a target=\"_blank\" href=\"https://maps.google.com/?q=%s,%s\">Map</a> " % (SITE[4], SITE[3]))
        output += ("<a target=\"_blank\" href=\"https://maps.google.com/?t=k&q=%s,%s\">Satellite</a> " % (SITE[4], SITE[3]))
        output += "</td>"
        output += "</tr>"
    output += "</table>"
    output += "<p>Number of unprocessed messages: <a href=\"http://data.glacsweb.info/iridium\" target=\"_blank\">%d</a></p>\r\n" % DB.get_unprocessed_message_count()
    output += "<a href = \"data.py\"> Download data</a>"
    output += "</body></html>"
    return output
