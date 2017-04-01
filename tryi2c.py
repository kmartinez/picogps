# main.py 
# i2c tests

import pyb
import utime
from machine import Pin
from pyb import I2C

data = bytearray(8)
# 
# use bus 2
i2c = I2C(2, I2C.MASTER)
i2c.init(I2C.MASTER, baudrate=20000) 

# i2c.deinit() # turn off peripheral

# read 1 bytes from deviceID 42 starting from addr 0 
print(i2c.mem_read(1, 0x102, 0))

