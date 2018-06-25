import pyproj

def convertwgs94(lon, lat, alt):
    #https://gis.stackexchange.com/a/212727/30004
    wgs84 = pyproj.Proj(
        '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')##4326
    geocentric= pyproj.Proj(
        '+proj=geocent +datum=WGS84 +units=m +no_defs')##4978
    x, y, z = pyproj.transform(wgs84, geocentric, lon, lat, alt)
    return (x, y, z)
