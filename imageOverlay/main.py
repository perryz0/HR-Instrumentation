# Adam Friesz, Husky Robotics
# Last Updated 1/20/24

# This class implements functions from overlay.py to display user or file input over the 
# given image file in a reasonable size in the bottom right corner. 
# The larger the given image file the longer the program will take to execute, a reasonable
# upper limit is 1.75 seconds. Linear increase in time based on number of pixels.

from overlay import overlay_text_bottom_right
from imgdata import get_gps_location, set_gps_location
from PIL import Image

#under = Image.open(input("Background image: "))
#text = read_json(input("Text file to display: "))
#text = input("Input text: ")

file = "exImages/P1030462.JPG"
latitude = 38.8951 
longitude = -77.0364
altitude = 1.1234
#set_gps_location(file, latitude, longitude, altitude)
#print(get_gps_location(file))

under = Image.open(file)
text = get_gps_location(file)

final = overlay_text_bottom_right(under, text)
final.save("exImages/composite.jpg");
