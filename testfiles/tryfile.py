# main.py 
# test file I/O

import os

def version():
	print('kirks file test code')

def writeit():
	#somedata = '0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
	somedata = '01234567890,1234567890,1234567890,3,4,5;'
	somedatasize = len(somedata)
	f = open('data.txt','a')
	for x in range(0,2):
		for y in range(0,10):
			written = f.write(somedata)	
		if written != somedatasize :
			print( 'write not complete')
	f.close()

def readit():
	f = open('data.txt','r')
	contents = f.read()
	# really need contents = f.readln()
	print( contents)
	print( len(contents))
	f.close()

def ls():
	print(os.listdir() )
