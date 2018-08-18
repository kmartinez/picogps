from math import pow, sqrt
from coordconvert import convertwgs94
TIME_INDEX = 2
LON_INDEX = 3
LAT_INDEX = 4
ALT_INDEX = 5
def add_dist_vel(data):
    reading_count = len(data)
    if reading_count >= 2:
        processed_data = []
        processed_data.append([])
        processed_data[0].extend(data[0])
        (prev_x, prev_y, prev_z) = convertwgs94(
            data[0][LON_INDEX], data[0][LAT_INDEX], data[0][ALT_INDEX])
        processed_data[0].extend([prev_x, prev_y, prev_z])
        prev_time = data[0][TIME_INDEX]
        i = 1   #skip the first row as no previous data
        while i < reading_count:
            (x, y, z) = convertwgs94(
                data[i][LON_INDEX], data[i][LAT_INDEX], data[i][ALT_INDEX])
            time = data[i][TIME_INDEX]
            time_diff = (time - prev_time).total_seconds()
            diff_x = x - prev_x
            diff_y = y - prev_y
            diff_z = z - prev_z
            diff_sum = pow(diff_x, 2) + pow(diff_y, 2) + pow(diff_z, 2)
            movement = sqrt(diff_sum)
            speed = movement / time_diff
            print "X = " + str(x)
            print "Y = " + str(y)
            print "Z = " + str(z)
            print "M = " + str(movement)
            print "S = " + str(speed)
            processed_data.append([])
            processed_data[i].extend(data[i])
            processed_data[i].extend([x, y, z, movement, speed])   #Add the calculated values to the row
            prev_x = x
            prev_y = y
            prev_z = z
            prev_time = time
            i += 1  #move onto the next record
        return processed_data
    return data
    # if only 1 reading cannot calc differences so return original data



