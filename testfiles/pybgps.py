from gps import *
from time import sleep
import lcd160cr
lcd = lcd160cr.LCD160CR('X')
def lcdinit():
    lcd.set_orient(lcd160cr.LANDSCAPE)
    #Set the position for text output using lcd.write()
    lcd.set_pos(20,70)
    #set text colow
    lcd.set_text_color(lcd.rgb(255, 0, 0), lcd.rgb(0, 0, 0))
    #set test font
    lcd.set_font(1)
    #Erase the entire display to the pen fill color.
    lcd.erase()
    lcd.set_pos(10, 10)
    #Write text to the display
    lcd.write('Glacsweb dGPS\r\n')
    lcd.set_text_color(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0))
    lcd.set_pos(20, 90)
    lcd.set_font(2)

def printfield(txt,n):
    lcd.set_pos(5,10+n*10)
    lcd.write(txt)

# running average of all values added
class averagepos:
    def __init__(self):
        self.lat_sum =0
        self.lon_sum =0
        self.alt_sum =0
        self.readings =0

    def add(self,lat,lon,alt):
        self.lat_sum += lat
        self.lon_sum += lon
        self.alt_sum += alt
        self.readings += 1
        return(self.lat_sum/self.readings, self.lon_sum/self.readings, self.alt_sum/self.readings)
    def clear(self):
        self.lat_sum = 0
        self.lon_sum = 0
        self.alt_sum = 0
        self.readings = 0

lcdinit()

gpsuart = pyb.UART(6,9600)
gpsuart.init(9600,bits=8,parity=None,timeout=60)
avpos = averagepos()
while(1):
        if gpsuart.any() :
            # its possible to read a stump if we don't wait
            sleep(0.2)
            nmea = gpsuart.readline()
            if (nmea == None) or (len(nmea) < 32):
		    continue
            pyb.LED(4).on() # lets flash blue LED
            try:
                thetype, data = processGPS(nmea)
            except:
                print('processGPS error - continuing.')
                continue
            #print(str(dat))
            print(data)
            if(thetype=='p'):
                #We got some positional data
                (lat,lon,alt,qual,hdop,sats,nmeafix) = data
                #print('Quality: ', qual,lat,lon,alt)
                printfield('%.8f' % lat,2)
                printfield('%.8f' % lon,3)
                printfield(alt,4)
                printfield(qual + " " + sats,5)
                #printfield('%.2f' % alt,4)
                lata, lona, alta = avpos.add(lat,lon, float(alt))
                print(lata,lona,alta)

            pyb.LED(4).off()
        sleep(0.3)
# Save is pressed - store value at end of points.txt file
#log = open('/sd/points.txt', 'a')
#log.write('\r\n')
#close file
#log.close()


