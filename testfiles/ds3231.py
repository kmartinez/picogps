# Pyboard driver for DS3231 precison real time clock.
# Adapted from WiPy driver at https://github.com/scudderfish/uDS3231
# Includes routine to calibrate the Pyboard's RTC from the DS3231
# delta method now operates to 1mS precision
# precison of calibration further improved by timing Pyboard RTC transition
# Adapted by Peter Hinch, Jan 2016
# stripped down to i2c bus 2 by Kirk

import utime, pyb
DS3231_I2C_ADDR = 104

class DS3231Exception(OSError):
    pass

rtc = pyb.RTC()

def now():  # Return the current time from the RTC in millisecs from year 2000
    secs = utime.time()
    ms = 1000 * (255 -rtc.datetime()[7]) >> 8
    if ms < 50:                                 # Might have just rolled over
        secs = utime.time()
    return 1000 * secs + ms

def nownr():  # Return the current time from the RTC: caller ensures transition has occurred
     return 1000 * utime.time() + (1000 * (255 -rtc.datetime()[7]) >> 8)

# Driver for DS3231 accurate RTC module (+- 1 min/yr) needs adapting for Pyboard
# source https://github.com/scudderfish/uDS3231
def bcd2dec(bcd):
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

def dec2bcd(dec):
    tens, units = divmod(dec, 10)
    return (tens << 4) + units

class DS3231:
    def __init__(self):
        self.ds3231 = pyb.I2C(2, mode=pyb.I2C.MASTER, baudrate=400000)
        self.timebuf = bytearray(7)
	# THIS COULD BE TIME CONSUMING?! KM ??
        if DS3231_I2C_ADDR not in self.ds3231.scan():
            raise DS3231Exception("DS3231 not found on I2C bus at %d" % DS3231_I2C_ADDR)

    def get_time(self, set_rtc = False):
        if set_rtc:
            data = self.await_transition()      # For accuracy set RTC immediately after a seconds transition
        else:
            data = self.ds3231.mem_read(self.timebuf, DS3231_I2C_ADDR, 0) # don't wait
        ss = bcd2dec(data[0])
        mm = bcd2dec(data[1])
        if data[2] & 0x40:
            hh = bcd2dec(data[2] & 0x1f)
            if data[2] & 0x20:
                hh += 12
        else:
            hh = bcd2dec(data[2])
        wday = data[3]
        DD = bcd2dec(data[4])
        MM = bcd2dec(data[5] & 0x1f)
        YY = bcd2dec(data[6])
        if data[5] & 0x80:
            YY += 2000
        else:
            YY += 1900
        if set_rtc:
            rtc.datetime((YY, MM, DD, wday, hh, mm, ss, 0))
        return (YY, MM, DD, hh, mm, ss, wday -1, 0) # Time from DS3231 in time.time() format (less yday)

    def copy_int_rtc(self):
        (YY, MM, DD, wday, hh, mm, ss, subsecs) = rtc.datetime()
        self.ds3231.mem_write(dec2bcd(ss), DS3231_I2C_ADDR, 0)
        self.ds3231.mem_write(dec2bcd(mm), DS3231_I2C_ADDR, 1)
        self.ds3231.mem_write(dec2bcd(hh), DS3231_I2C_ADDR, 2)      # Sets to 24hr mode
        self.ds3231.mem_write(dec2bcd(wday), DS3231_I2C_ADDR, 3)    # 1 == Monday, 7 == Sunday
        self.ds3231.mem_write(dec2bcd(DD), DS3231_I2C_ADDR, 4)
        if YY >= 2000:
            self.ds3231.mem_write(dec2bcd(MM) | 0b10000000, DS3231_I2C_ADDR, 5)
            self.ds3231.mem_write(dec2bcd(YY-2000), DS3231_I2C_ADDR, 6)
        else:
            self.ds3231.mem_write(dec2bcd(MM), DS3231_I2C_ADDR, 5)
            self.ds3231.mem_write(dec2bcd(YY-1900), DS3231_I2C_ADDR, 6)

    # set the M4 rtc then copy to the ds3231 DANGER its .init in uPython 1.9
    def set_time(self, YY, MM, DD, wday, hh, mm, ss) :
    	rtc.datetime((YY, MM, DD, wday, hh, mm, ss, 0))
    	self.copy_int_rtc()

    def delta(self):                            # Return no. of mS RTC leads DS3231
        self.await_transition()
        rtc_ms = now()
        t_ds3231 = utime.mktime(self.get_time())  # To second precision, still in same sec as transition
        return rtc_ms - 1000 * t_ds3231

    def await_transition(self):                 # Wait until DS3231 seconds value changes
        data = self.ds3231.mem_read(self.timebuf, DS3231_I2C_ADDR, 0)
        ss = data[0]
        while ss == data[0]:
            data = self.ds3231.mem_read(self.timebuf, DS3231_I2C_ADDR, 0)
        return data

    def setalarm(self,hour):
        self.ds3231.mem_write(dec2bcd(hour), DS3231_I2C_ADDR, 9)
    	# min and seconds  must be zero
        self.ds3231.mem_write(0, DS3231_I2C_ADDR, 8) #minutes
        self.ds3231.mem_write(0, DS3231_I2C_ADDR, 7) #seconds
    	# also need to set A1M4 3 2 1 bits to 1000 for HH Min Sec match alarm
        self.ds3231.mem_write(128, DS3231_I2C_ADDR, 0xa) #SET ALM4

        #Finally, set alarm enable and interrupt output option
        self.ds3231.mem_write(5, DS3231_I2C_ADDR, 0xe) #SET INTCN and A1IE

    	h = self.ds3231.mem_read(1,DS3231_I2C_ADDR,9)
    	s = self.ds3231.mem_read(1,DS3231_I2C_ADDR,0xa)
    	print(h, s)
    	
    def clearalarm(self):
        self.ds3231.mem_write(0, DS3231_I2C_ADDR, 0xe)
        self.ds3231.mem_write(0, DS3231_I2C_ADDR, 0xf)
	

    def testalarm(self):
    	self.set_time(2017,1,1,1,11,59,50)
    	self.setalarm(12)
