#!/usr/bin/env python
# try Rockblock sat coms on UART 1 (tiny pins)
# for normal systems: import serial
# may have to disable handshake with AT&K0 ???
# may have to read back the stuff sent as its echod
from pyb import UART
import utime

# normal systems:
#ser = serial.Serial('/dev/ttyUSB0',19200)
ser = UART(2,19200)
# can set the timeout option too somehow

# gives 0 none to 5 strong, updated avery few s
def satsignal():
	print('getting signal strength')
	ser.write('AT+CSQ\r')
	print(ser.read())

def waitforOK():
	count = 10
	while count > 0 :
		ret = ser.read()
		if ret == None:
			count = count - 1
		else:
			return(True)
	return(False)
		
def waitforsat():
	count = 10
	print('sending AT')
	ser.write('AT\r')
	while count > 0:
		#utime.sleep_ms(200)
		ret = ser.read()
		if ret == None:
			print('nothing yet')
		else:
			print(ret)
			count = 0

def sendtext(msg): 
	print('sending message')
	txt = msg + '\r'
	ser.write(txt)
	waitforOK()

def sendmsg(msg): 
	print('sending message')
	txt = 'AT+SBDWT=' + msg + '\r'
	ser.write(txt)
	waitforOK()
	# was it ok?
	ser.write('AT+SBDIX\r')
	ret = ser.read()
	# shoud be +SBDIX: 0,0,0,0,0,0\r
	print(ret)


