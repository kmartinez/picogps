#!/usr/bin/env python
# use Rockblock sat coms on UART 1 (tiny pins)
# may have to disable handshake with AT&K0 ???
# have to read back anything sent as its echod
from time import sleep
import pyb
from utime import sleep_ms
from common import d
# gives 0 none to 5 strong
# after few s it replies +CSQ:2 newline then OK
# We NEED TO INHERIT THIS FROM BOOT?
satuart = pyb.UART(2,19200)
satuart.init(19200,bits=8,parity=None,timeout=60)
# sig str can take > 4s
# VERY BUGGY AT THE MOMENT!
def satsignal():
	print('getting signal strength')
	msg = 'AT+CSQ\r'
	satuart.write(msg)
	#discard our echo
	#satuart.readline()
	#discard blank line
	#ret = satuart.readline()
	#d(ret)
	#sleep(1)
	#ret = satuart.readline()
	#d(ret)
	#OK
	#ret = satuart.readline()
	#d(ret)
	# now we hope for reply
	# at some read we will get CSQ:3\r\n
	count = 60
	while count > 0:
		ret = str(satuart.readline())
		d(ret)
		csqpos = ret.find("CSQ:")
		if (csqpos >= 0) and (len(ret) >5) :
			return ( ret[4 + csqpos] )
		count = count -1
		sleep_ms(100)
	return(0)

def waitforOK():
	count = 20
	while count > 0 :
		ret = satuart.read()
		if ret == None:
			count = count - 1
			sleep_ms(50)
		else:
			d('got OK')
			return(True)
	return(False)
		
# mainly in case it hasn't started up yet
def waitforsat():
	count = 10
	while count > 0:
		print('sending AT')
		satuart.write('AT\r')
		#discard our echo
		satuart.readline()
		#utime.sleep_ms(200)
		sleep(1)
		ret = satuart.readline()
		if ret != None:
			d(ret)
			count = 0
		else:
			count = count -1
			print('nothing yet')

def sendtext(msg): 
	print('sending message')
	txt = msg + '\r'
	satuart.write(txt)
	#waitforOK()
	print(satuart.read())

# send a msg - can take many seconds
def sendmsg(msg): 
	print('sending message')
	txt = 'AT+SBDWT=' + msg + '\r'
	satuart.write(txt)
	waitforOK()
	sleep(1)
	# was it ok?
	satuart.write('AT+SBDIX\r')
	#discard our echo
	satuart.readline()
	# probably need sleep 1 or 2
	sleep(1)
	count = 10
	while count > 0 :
		ret = satuart.read()
		# SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
		# FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
		print(ret)
		if ret != None:
			status = ret.split(",")[0].split(" ")[1]
			if status == "0":
				d("msg sent")
			return(True)
		count = count - 1
		sleep_ms(100)

