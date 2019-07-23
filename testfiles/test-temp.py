# read analogue temp sensor on Pico
# conversion for LMT86LPG
# http://www.ti.com/lit/ds/symlink/lmt86.pdf
# sensor is +- 0.4 to 0.7C so can round to one decimal place
# Kirk Martinez and Denise Yap 2018
import math
from time import sleep
from pyb import Pin
from pyb import RTC

a = pyb.ADC(pyb.Pin.board.A5)
g = pyb.Pin('A7', pyb.Pin.OUT_PP)
rtc = RTC()

# set a specific date and time
rtc.datetime((2019, 7, 27, 5, 15, 42, 0, 0)) 

#Tuen on lmt86
print('LMT86 turn on.')
g.high()
#must wait 2ms before use
sleep(0.02)
#Check ADC value 
def adcValue():	
	adcVal = a.read()
	return adcVal

#Convert ADC value to mV
#def mV():
	# convert adc to mV using 3300mV as Vcc
	#tmp = a.read()
	#v = tmp * 3300 / 4096.0	
	#tc = ((10.888 - math.sqrt(118.548544 + 0.01388 * (1777.3 -v)))/-0.00694) + 30			
	#return v
	#return(round(tc,1))

#Convert adc to degree celcius
def lmt86():
	mv = a.read() * 3300.0 / 4096.0
	tc2 = ((10.888 - math.sqrt(118.548544 + 0.01388 * (1777.3 - mv)))/-0.00694) + 30
	return tc2
	#return(round(tc2,1))

#Use mean to minimize white noise	
def meantemp():
	n = 0.0
	for count in range(1,10):
		n = n + lmt86()
	return(round(n/10.0,1))

def rtcc():
	r = rtc.datetime() # get date and time
	return r

#while True:
	#print(lmt86())
	#sleep(1)	

#Print meantemp for 100 times	
for count in range(1,100):
	#print('Date and Time : ')
	#print(rtcc())
	print('meantemp : ')
	print(meantemp())
	sleep(2)

#Turn off lmt86
print('lmt86 turn off.')
g.low()	
