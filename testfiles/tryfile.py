# main.py 
# test file I/O

import os

def version():
	print('kirks file test code')

def writeit():
	somedata = '01234567890,1234567890,1234567890,3,4,5\n'
	somedatasize = len(somedata)
	f = open('data.txt','a')
	for y in range(0,10):
		written = f.write(somedata)	
		print(written)
	if written != somedatasize :
		print( 'write not complete')
	f.close()

def readit():
	data = []
	payload = ""

	with open('data.txt','r') as file:
		i = 0
		for line in file:
			# need to swap \n for ; for iridium
                        linenoCR = line.rstrip('\n')
                        linenoCR = linenoCR + ';'
                        payload = payload + linenoCR
                        #Check we are only sending a few readings.
                        i = i + 1
                        if(i >= 5):
                                break
	print(i)
	file.close()
	# fake sat send
	print(payload)
	# if success
	file= open('data.txt','r')
	count = i
	# read the lines we sent
	while( count > 0):
		file.readline()
		count -= 1
	restoffile = file.read()
	file.close()
	file = open('data.txt','w')
	file.write(restoffile)
	file.close()

def ls():
	print(os.listdir() )
