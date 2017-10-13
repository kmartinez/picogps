# haversine formula to get dist between two long lats
from math import radians, sin, cos, atan2, sqrt

def haver(lat1, lon1, lat2, lon2):
	R = 6371000
	lat1r = radians(lat1)
	lat2r = radians(lat2)
	dlat = radians(lat2 - lat1)
	dlon = radians(lon2 - lon1)
	a = (sin(dlat/2) * sin(dlat/2) 
	+ cos(lat1r) * cos(lat2r)
	* sin(dlon/2) * sin(dlon/2) )
	c = 2 * atan2(sqrt(a),sqrt(1-a))
	d = R * c
	return d

print(haver(64.0937139,-16.33418481,  64.09371249,-16.33418175 ) )


