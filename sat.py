#!/usr/bin/env python
# try Rockblock sat coms on UART 1 (tiny pins)
# for normal systems: import serial
# may have to disable handshake with AT&K0 ???
# may have to read back the stuff sent as its echod
#from pyb import UART
#import serial
#import utime
#ser = UART(2,19200)

# normal systems:
from time import sleep
import pyb
# ser = serial.Serial('/dev/ttyUSB0',19200)
# can set the timeout option too in ms:
# ser.init(19200,nits=8,parity=None,timeout=50)

# gives 0 none to 5 strong
# after few s it replies +CSQ:2 newline then OK

ser = pyb.UART(2,19200)

# sig str can take > 4s
def satsignal():
	print('getting signal strength')
	msg = 'AT+CSQ\r'
	ser.write(msg)
	# give it time so we dont timeout
	#utime.sleep_ms(100)
	sleep(4)
	#discard our echo
	ser.readline()
	ret = ser.readline()
	#blank line
	ser.readline()
	#OK
	ret = str(ret)
	ser.readline()
	if ret != None:
		n =  ret.find('+CSQ')
		if n != -1:
			#print(ret.strip())
			return( int(ret[n+5:n+5+1]) )
	else:
		return(None)

def waitforOK():
	count = 10
	while count > 0 :
		ret = ser.read()
		if ret == None:
			count = count - 1
		else:
			return(True)
	return(False)
		
# mainly in case it hasn't started up yet
def waitforsat():
	count = 10
	while count > 0:
		print('sending AT')
		ser.write('AT\r')
		#discard our echo
		ser.readline()
		#utime.sleep_ms(200)
		sleep(1)
		ret = ser.readline()
		if ret != None:
			print(ret)
			count = 0
		else:
			print('nothing yet')

def sendtext(msg): 
	print('sending message')
	txt = msg + '\r'
	ser.write(txt)
	#waitforOK()
	print(ser.read())

# send a msg - can take many seconds
def sendmsg(msg): 
	print('sending message')
	txt = 'AT+SBDWT=' + msg + '\r'
	ser.write(txt)
	waitforOK()
	# was it ok?
	ser.write('AT+SBDIX\r')
	#discard our echo
	ser.readline()
	# probably need sleep 1 or 2
	ret = ser.read()
	# SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
	# FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
	print(ret)
	status = ret.split(",")[0].split(" ")[1]
	if status == "0":
		d("msg sent")


# waitforsat(ser)

# strength = satsignal()
# if strength != None:
# 	print strength
