# test Iridium coms
# copy to main.py
from sat import *
from time import sleep

Satpower.value(1)

waitforsat()

count = 3
while count > 0:
	sig = satsignal()
	print( sig)
	if int(sig) > 1:
		sendmsg('first auto test message')
		count = 0
	else:
		count = count -1
