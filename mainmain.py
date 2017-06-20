#
# main picoGPS code

# just been woken up by alarm

# check we are on a scheduled hour
schedule = (0, 3, 6, 9, 12, 15, 18,21)

# if not we're in maintenance mode exit()

# turn on GPS
# wait for GPS fix OR timeout - store
# turn GPS off

# if gpstime is > 10s different from extrtc - set extrtc

# turn SAT on
# send fix via sat
# turn SAT off

# if not successful 
#  store GPS fix in the file (check file is not at maxsize)

# set next wakeup from schedule

# if we are not on USB:
# deepsleep
# pyb.stop()
