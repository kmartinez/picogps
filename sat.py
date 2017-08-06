#!/usr/bin/env python
# use Rockblock sat coms on UART 1 (tiny pins)
# may have to disable handshake with AT&K0 ???
# have to read back anything sent as its echod
from time import sleep
import pyb
# gives 0 none to 5 strong
# after few s it replies +CSQ:2 newline then OK
satuart = pyb.UART(2,19200)
# sig str can take > 4s
def satsignal():
	print('getting signal strength')
	msg = 'AT+CSQ\r'
	satuart.write(msg)
	# give it time so we dont timeout
	#utime.sleep_ms(100)
	sleep(4)
	#discard our echo
	satuart.readline()
	ret = satuart.readline()
	#blank line
	satuart.readline()
	#OK
	ret = str(ret)
	satuart.readline()
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
		ret = satuart.read()
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
		satuart.write('AT\r')
		#discard our echo
		satuart.readline()
		#utime.sleep_ms(200)
		sleep(1)
		ret = satuart.readline()
		if ret != None:
			print(ret)
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
	# was it ok?
	satuart.write('AT+SBDIX\r')
	#discard our echo
	satuart.readline()
	# probably need sleep 1 or 2
	ret = satuart.read()
	# SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
	# FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
	print(ret)
	status = ret.split(",")[0].split(" ")[1]
	if status == "0":
		d("msg sent")


