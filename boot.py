# boot.py -- run on boot-up
# set up default I/O states and naming

import machine
import pyb
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
#pyb.usb_mode('VCP+HID') # act as a serial device and a mouse

GPSpower = pyb.Pin('B13',Pin.OUT)
Satpower = pyb.Pin('B14',Pin.OUT)
gpsuart = UART(1,38400)
satuart = UART(2,19200)

