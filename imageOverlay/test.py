# contains testing code

from overlay import *
from imgdata import *
from PIL import Image

file = "exImages/composite.jpg"
# image = Image.open(file)
# final = overlayScalebar(image, "tl")

# final.save("exImages/scalebar-ex.jpg")

latitude = 38.8951 
longitude = -77.0364
altitude = 1.1234

#set_gps_location(file, latitude, longitude, altitude)
#print(get_gps(file))
print(get_gps_location(file))

# under = Image.open(input("Background image: "))
# text = input("Text file to display: ")
# text = input("Input text: ")

# file = "exImages/P1030462.JPG"
# latitude = 38.8951 
# longitude = -77.0364
# altitude = 1.1234
# #set_gps_location(file, latitude, longitude, altitude)
# #print(get_gps_location(file))

# under = Image.open(file)
# text = get_gps_location(file)

# final = overlayText(under, text, 'br')
# final.save("exImages/composite.jpg");