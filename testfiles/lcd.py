# print fields on the little lcd screen
# designed for lat lon alt sats

import lcd160cr
import time

#Construct an LCD160CR object
lcd = lcd160cr.LCD160CR('X')
#Set the orientation of the display. Can be PORTRAIT,LANDSCAPE,POTRAIT_UPSIDEDOWN,LANDSCAPE_UPSIDEDOWN
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
#lcd.write('Hello World!')
def printfield(txt,n):
    lcd.set_pos(5,10+n*10)
    lcd.write(txt)

lat = 60.12345678
lon = 12.3456789
alt = 100.1
printfield("P1",1)
while True:
    printfield('%.8f' % lat,2)
    printfield('%.8f' % lon,3)
    printfield('%.2f' % alt,4)
    time.sleep(0.5)
    lat = lat + 0.1
    alt = alt + 0.1

#create and open a .txt file, set to write mode
#log = open('/sd/log.txt', 'w')
#write to txt file
#log.write('test start')
#log.write('\r\n')
#close file
#log.close()

#log = open('/sd/log.txt', 'a')
#log.write('test end')
#log.close()
