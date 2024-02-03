# Adam Friesz, Husky Robotics
# Last Updated 2/2/24

# This class implements functions from overlay.py and imgdata.py to guide user's through 
# overlaying gps coordinates and scalebars on a given image.

from overlay import overlayText, overlayScalebar
from imgdata import get_gps_location, set_gps_location
from PIL import Image

mode = ""
print("This program allows users to add gps and scalebar information to their image.")
filepath = input("What image would you like to work with? Paste filepath: ")
print("\n")

while (mode != 'quit'):
    mode = input("Would you like to use the (gps) or (scalebar)? ")
    if mode == 'gps':
        a = input("  Would you like to (read), (write), or (overlay) gps info? ")
        if a == 'read':
            try:
                print(get_gps_location("     " + filepath))
            except:
                print("     No GPS data is written on this file.")
        elif a == 'write':
            lat = float(input("     Latitude? "))
            lng = float(input("     Longitude? "))
            alt = float(input("     Altitude? "))
            set_gps_location(filepath, lat, lng, alt)
            print("     GPS written: " + get_gps_location(filepath))
        elif a == 'overlay':
            newpath = filepath[: filepath.index('.')] + '-gps.jpg'
            img = overlayText(Image.open(filepath), get_gps_location(filepath), 'br')
            img.save(newpath)
            print("     Image saved as: " + newpath)
    elif mode == 'scalebar':
        img = overlayScalebar(Image.open(filepath), 'br')
        newpath = filepath[: filepath.index('.')] + '-scalebar.jpg'
        img.save(newpath)
        print("     Image saved " + newpath)
    else:
        print("Invalid input.")

    print("\n")
    mode = input("Would you like to (continue) or (quit)?")