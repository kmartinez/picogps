# simple test of reading UART 1 on Pico
from pyb import UART

# speed is set in ucenter for uart1probably 115200?
ser = UART(1,9600)
# hopefully read nmea header
while 1:
	s = ser.readline()
	print s
