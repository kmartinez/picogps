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
# try three times in case its increasing
def satsignal():
	maincount = 3
	while maincount > 0:
		d('getting signal strength')
		msg = 'AT+CSQ\r'
		satuart.write(msg)
		# this will discard our echo, blank line etc
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
		sleep(2)
		maincount = maincount - 1
	return(0)

# wait until message sent return and parse code
# SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
# FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
def waitforsentOK():
	count = 200
	while count > 0:
		ret = str(satuart.readline())
		d('Count is '+ str(count))
		d(ret)
		pos = ret.find("+SBDIX:")
		d(pos)
		if (pos >= 0) and (len(ret) >5) :
			fields = ret.split(',')
			rcode = fields[0].split(' ')[1]
			d(rcode)
			if rcode == '0':
				return ( True )
		count = count -1
		sleep_ms(100)
	return(False)

def waitforREADY():
	count = 20
	while count > 0 :
		ret = satuart.read()
		if ret == None:
			count = count - 1
			sleep_ms(50)
		else:
			ret = str(ret)
			if ret.find("READY") > 0:
				d('got READY')
				return(True)
	return(False)

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
		
# wait for Sat to be responsive - allow for lock
def waitforsat():
	count = 10
	while count > 0:
		sleep(1)
		d('sending AT')
		satuart.write('AT\r')
		#discard our echo
		satuart.readline()
		#utime.sleep_ms(200)
		ret = satuart.readline()
		if ret != None:
			d(ret)
			count = 0
		else:
			count = count -1
			d('nothing yet')

# send a msg - can take many seconds
def sendmsg(msg): 
	d('sending message')
	#txt = 'AT+SBDWT=' + msg + '\r'
	#satuart.write(txt)
	#waitforOK()
	satuart.write('AT+SBDWT\r')
	waitforREADY()
	txt = msg + '\r'
	satuart.write(txt)
	sleep(1)
	# was it ok?
	satuart.write('AT+SBDIX\r')
	#discard our echo
	satuart.readline()
	# probably need sleep 1 or 2
	sleep(1)
	count = 200
	if waitforsentOK():
		d('message sent')
		return(True)
	else:
		d('message failed')
		return(False)

	#while count > 0 :
	#	ret = satuart.readline()
		# SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
		# FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
	#	if (ret != None) and (len(ret) > 6) :
	#		ret = ret.lstrip()
	#		print(ret)
			# SOME BUG IN HERE TO DO WITH binary/strings
	#		satstatus = ret.split(",")[0].split(" ")[1]
	#		if satstatus == "0":
	#			d("msg sent")
	#		return(True)
	#	count = count - 1
	#	sleep_ms(100)

