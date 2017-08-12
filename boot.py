# boot.py -- run on boot-up
# set up default I/O states and naming

import machine
import pyb

gpspower = pyb.Pin('B13',machine.Pin.OUT)
satpower = pyb.Pin('B14',machine.Pin.OUT)
gpsuart = pyb.UART(1,9600)
satuart = pyb.UART(2,19200)
