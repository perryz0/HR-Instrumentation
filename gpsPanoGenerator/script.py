# Perry Chien, Adam Friesz, Husky Robotics, PY 2024
# Last updated 5/23/24

# This script takes in an image folder as an input directly from the terminal
# and generates a panorama with one single GPS coordinate annotated on it.

import sys
from stitching import Stitcher
import os
from PIL import Image
import numba
from overlay import overlayText
from imgdata import set_gps_location, get_gps_location

numba.config.DISABLE_JIT = True  # Disable Numba JIT caching

# inner GPSHandler class to help with GPS overlay onto pano
class GPSHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_gps(self):
        try:
            return get_gps_location(self.filepath)
        except:
            return "No GPS data is written on this file."

    def write_gps(self, lat, lng, alt):
        set_gps_location(self.filepath, lat, lng, alt)
        return get_gps_location(self.filepath)

    def overlay_gps(self, gps_data):
        newpath = self.filepath[:self.filepath.index('.')] + '-gps.jpg'
        img = overlayText(Image.open(self.filepath), gps_data, 'br')
        img.save(newpath)
        return newpath

def get_real_time_gps():
    # placeholder function to fetch real-time GPS coordinates.
    # replace with actual implementation of WebSocket communication stuff to get GPS data.
    # return: (latitude, longitude, altitude)
    return (47.6062, -122.3321, 15.0)

if len(sys.argv) != 2:
    print("Usage: python script.py <Image folder path>")
    sys.exit(1)

path = sys.argv[1]
files = []

for entry in os.listdir(path):
    pentry = os.path.join(path, entry)
    try:
        Image.open(pentry)
        files.append(pentry)
    except IOError:
        print(entry, "is not an image and was skipped.")

if not files:
    raise Exception("There are no images to stitch.")

try:
    stitcher = Stitcher()
    panorama = stitcher.stitch(files)

    # save pano image
    panorama_path = os.path.join(path, "panorama.jpg")
    im = Image.fromarray(panorama)
    im.save(panorama_path)
    print(f"Panorama saved as: {panorama_path}")

    # obtain real-time GPS coordinates
    lat, lng, alt = get_real_time_gps()

    # create an instance of GPSHandler for the panorama image
    gps_handler = GPSHandler(panorama_path)

    # write the GPS coordinates to the image
    gps_handler.write_gps(lat, lng, alt)

    # overlay the GPS data on the panorama image
    newpath = gps_handler.overlay_gps(gps_handler.read_gps())
    print(f"Panorama with GPS overlay saved as: {newpath}")

except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
    raise e
except KeyError as e:
    print(f"Key error: {e}")
    raise e