#!/usr/bin/env python
# try Rockblock sat coms on UART 2 (tiny pins)
# for bare pico swap to uart 1 (gps uart normally)
# for laptop systems: import serial
# may have to disable handshake with AT&K0 ???
# may have to read back the stuff sent as its echod
#from pyb import UART
#import utime
#assume we have imported pyb
from sat import *
satuart = pyb.UART(1,19200)
satuart.init(19200,bits=8,parity=None,timeout=60)
# normal systems:
#import serial
from time import sleep
#ser = serial.Serial('/dev/ttyUSB0',19200)
# can set the timeout option too in ms:
# ser.init(19200,bits=8,parity=None,timeout=50)

# gives 0 none to 5 strong
# after few s it replies +CSQ:2 newline then OK
def satsignal0():
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
	ret = str(satuart.readline())
	if ret != None:
		n =  ret.find('+CSQ')
		if n != -1:
			#print(ret.strip())
			return( int(ret[n+5:n+5+1]) )
	else:
		return(None)

def waitforOK0():
	count = 10
	while count > 0 :
		ret = satuart.read()
		if ret == None:
			count = count - 1
		else:
			return(True)
	return(False)
		
def waitforsat0():
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
			print('nothing yet')

def sendtext0(msg): 
	print('sending message')
	txt = msg + '\r'
	satuart.write(txt)
	#waitforOK()
	print(satuart.read())

def sendmsg0(msg): 
	print('sending message')
        txt = 'AT+SBDWT=' + msg + '\r'
        satuart.write(txt)
        waitforOK()
        # was it ok?
        satuart.write('AT+SBDIX\r')
        #discard our echo
        satuart.readline()
        # probably need sleep 1 or 2
	sleep(2)
	ret = None
        while (ret != None) :
		ret = satuart.readline()
		sleep(1)
		print("waiting for status")
        # SUCCESS is +SBDIX: 0, 0, 0, 0, 0, 0
        # FAIL like +SBDIX: 32, 1, 2, 0, 0, 0
        print(ret)
        status = ret.split(",")[0].split(" ")[1]
        if status == "0":
                print("msg sent")

# send a binary bytearray
def sendbinarymsg(ba): 
	d('sending message')
        msg = appendchksum(ba)
	#txt = 'AT+SBDWT=' + msg + '\r'
	#satuart.write(txt)
	#waitforOK()
	satuart.write('AT+SBDWB=' + str(len(ba)) + '\r')
	waitforREADY()
	satuart.write(msg)
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

def appendchksum(ba):
    total = sum(ba)
    print(total)
    c = [(total & 0xff00) >> 8, total & 0xff]
    return( ba + bytearray(c) )

# just checks AT returns
waitforsat()
count = 1
while count < 10:
	strength = satsignal()
	if strength != None:
		print("strength=" + str(strength))
                if strength > 3 :
                    break
	count = count + 1
	sleep(1)


if strength > 3:
        data = [1,2,3,4,5,6,7,8]
        data_ba = bytearray(data)
	sendbinarymsg(data_ba)
