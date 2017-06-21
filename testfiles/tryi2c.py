# main.py 
# i2c tests

import pyb
import utime
from machine import Pin
from pyb import I2C

data = bytearray(16)
# 
# use bus 2
i2c = I2C(2, I2C.MASTER)
i2c.init(I2C.MASTER, baudrate=40000)

# i2c.deinit() # turn off peripheral

# read 10 bytes from deviceID 104 (our DS3231) starting from addr 0 
for n in range(0,10):
	b = i2c.mem_read(1, 104, n)
	print(b)
print(i2c.mem_read(1, 104, 0xe))
print(i2c.mem_read(1, 104, 0xf))

