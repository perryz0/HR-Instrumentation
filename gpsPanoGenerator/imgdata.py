import json
import os
import piexif
from fractions import Fraction

def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple

    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number):
    """convert a number to rational

    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


def set_gps_location(file_name, lat, lng, altitude):
    """Adds GPS position as EXIF metadata
        # GPS data will be stored in degrees, minutes, seconds format

    Keyword arguments:
    file_name -- image file
    lat -- latitude (as float)
    lng -- longitude (as float)
    altitude -- altitude (as float)

    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exiv_lng,
    }
    

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_name)

# returns dict of all gps data in image exif data
def get_gps(file):
    data = piexif.load(file)
    return data["GPS"]

# takes an image file and displays its encoded GPS code information.
# returns lat, lng coordinates in readable string format displayed in degree, minute, seconds format. 
# returns None if there is no GPS data.
def get_gps_location(file):
    data = piexif.load(file)
    if "GPS" in data.keys():
        GPS_info = data["GPS"]
        str_lat = str(GPS_info[2][0][0]) + "° " + str(GPS_info[2][1][0]) + "' " + \
                str(GPS_info[2][2][0] / GPS_info[2][2][1]) + "\" " + str(GPS_info[1])[2]

        str_lng = str(GPS_info[4][0][0]) + "° " + str(GPS_info[4][1][0]) + "' " + \
                str(GPS_info[4][2][0] / GPS_info[4][2][1]) + "\" " + str(GPS_info[3])[2]
        return str_lat + ", " + str_lng
    else: 
        return "None"

# reads a json file and returns a string containing its contents
def read_json(file):
    data = json.load(open(file))
    text = ""

    for dim in data.keys():
        text += dim + ': ' + str(data.get(dim))
    return text