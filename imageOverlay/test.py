from overlay import shade
from imgdata import *
#from imgdata import *
from PIL import Image
import piexif

file = "/Users/adamfriesz/Documents/UW/HRC/imageOverlay/exImages/moran-park.jpg"

# latitude = 38.8951 
# longitude = -77.0364
# altitude = 1.1234

set_gps_location(file, latitude, longitude, altitude)
print(get_gps(file))
#print(get_gps_location(file))