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
        output = "IMEI MUST BE SPECIFIED"
    else:
        output = """<html>
            <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {'packages':['corechart']});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {
                var data = google.visualization.arrayToDataTable([['timestamp','temperature'],"""

        data =  DB.get_sats(parameters.getfirst("imei"))
        for line in data:
            output += '[ new Date(' + str(int(line[1].strftime("%s")) * 1000)  + '),' + str(line[2]) + '],'
        # chop off final comma
        output = output[:-1]
        output += """]);
            var options = {"""
        output += "title: 'Iceland Glacier tracker satelite plot %s '," % parameters.getfirst("imei")
        output += """
          width: 1500,
          height: 1000,
              haxis: {title: 'timestamp'},
              vaxis: {title: 'satelites'},
              legend: 'none',
          explorer: {}
            };
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
    <div id="chart_div" style="width: 1600px; height: 1000px;"></div>
  </body>
</html>"""

    req.content_type = 'text/html'

    return output
