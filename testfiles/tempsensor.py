# read analogue temp sensor on Pico
# conversion for LMT86LPG
# http://www.ti.com/lit/ds/symlink/lmt86.pdf
# sensor is +- 0.4 to 0.7C so can round to one decimal place
import math
from time import sleep

a = pyb.ADC(pyb.Pin.board.A5)

def lmt86():
	# convert adc to mV using 3300mV as Vcc
	v = a.read() * 3300 / 4096.0
	tc = (10.888 - math.sqrt(118.548544 + 0.01388 * (1777.3 -v)))/-0.00694 + 30
	return(round(tc,1))
	
while True:
	print(lmt86() )
	sleep(1)
