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
g = pyb.Pin('B1', pyb.Pin.OUT_PP)
rtc = RTC()

# set a specific date and time
rtc.datetime((2018, 7, 27, 5, 15, 42, 0, 0)) 

#Tuen on lmt86
print('LMT86 turn on.')
g.high()

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

#Convert mV to degree celcius
def lmt86():
	tmp = a.read()
	w = tmp * 3300 / 4096.0
	tc2 = ((10.888 - math.sqrt(118.548544 + 0.01388 * (1777.3 - w)))/-0.00694) + 30
	return tc2
	#return(round(tc2,1))

#Use mean to minimize white noise	
def meantemp():
	n = 0.0
	for count in range(1,50):
		n = n + lmt86()
	return(round(n/50.0,1))

def rtcc():
	r = rtc.datetime() # get date and time
	return r

#while True:
	#print('lmt86 in mV : ')
	#print(mV())
	#print('lmt86 in temp : ')
	#print(lmt86())
	#print("adc val : ")
	#print(adcValue())
	#sleep(1)	

#Print meantemp for 100 times	
for count in range(1,10):
	print('Date and Time : ')
	print(rtcc())
	print('meantemp : ')
	print(meantemp())
	sleep(60)

#Turn off lmt86
print('lmt86 turn off.')
g.low()	
