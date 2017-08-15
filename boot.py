# boot.py -- run on boot-up
# set up default I/O states and naming

import machine
import pyb

gpspower = pyb.Pin('B13',machine.Pin.OUT)
satpower = pyb.Pin('B14',machine.Pin.OUT)
gpsuart = pyb.UART(1,9600)
gpsuart.init(9600,bits=8,parity=None,timeout=60)
satuart = pyb.UART(2,19200)
