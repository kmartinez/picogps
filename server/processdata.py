from math import pow, sqrt
from coordconvert import convertwgs84
TIME_INDEX = 2
LON_INDEX = 3
LAT_INDEX = 4
ALT_INDEX = 5
def add_dist_vel(data):
    totdist = 0
    reading_count = len(data)
    if reading_count >= 2:
        processed_data = []
        processed_data.append([])
        processed_data[0].extend(data[0])
        (first_x, first_y, first_z) = convertwgs84(
            data[0][LON_INDEX], data[0][LAT_INDEX], data[0][ALT_INDEX])
        processed_data[0].extend([first_x, first_y, first_z, 0, 0, 0])
        prev_x = first_x
        prev_y = first_y
        prev_z = first_z
        prev_time = data[0][TIME_INDEX]
        i = 1   #skip the first row as no previous data
        while i < reading_count:
            (x, y, z) = convertwgs84(
                data[i][LON_INDEX], data[i][LAT_INDEX], data[i][ALT_INDEX])
            time = data[i][TIME_INDEX]
            time_diff = (time - prev_time).total_seconds()
            diff_x = x - prev_x
            diff_y = y - prev_y
            diff_z = z - prev_z
            diff_sum = pow(diff_x, 2) + pow(diff_y, 2) + pow(diff_z, 2)
            movement = sqrt(diff_sum)
            total_x = x - first_x
            total_y = y - first_y
            total_z = z - first_z
            total_sum = pow(total_x,2) + pow(total_y, 2) + pow(total_z, 2)
            totdist = sqrt(total_sum)
            speed = movement / time_diff
            print "X = " + str(x)
            print "Y = " + str(y)
            print "Z = " + str(z)
            print "M = " + str(movement)
            print "S = " + str(speed)
            print "D = " + str(totdist)
            processed_data.append([])
            processed_data[i].extend(data[i])
            processed_data[i].extend([x, y, z, movement, speed, totdist])   #Add the calculated values to the row
            prev_x = x
            prev_y = y
            prev_z = z
            prev_time = time
            i += 1  #move onto the next record
        return processed_data
    return data
    # if only 1 reading cannot calc differences so return original data



