# Perry Chien
#
# Basically script.py but experimenting to fix color-change bugs after stitch (yellow to blue?)
# Still unknown reason...
#
# WIP refined version of the stitching script. Trying to address the color change issue
# (i.e. yellowish to blueish for no reason)

import sys
import cv2
import numpy as np
import os
import numba
from PIL import Image
import platform  # Import platform module for detecting OS

# Get the absolute path to the gpsPanoGenerator directory and add it to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Now the imports should work correctly
from src.image_processing.overlay import overlayText
from src.image_processing.imgdata import set_gps_location, get_gps_location
from src.gps.gps_handler import GPSHandler

from matplotlib import pyplot as plt

# disable Numba JIT caching (resolved debugger issue), check back later
numba.config.DISABLE_JIT = True

def plot_image(img, figsize_in_inches=(5,5)):
    fig, ax = plt.subplots(figsize=figsize_in_inches)
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

# normalize colors across a series of images (ATTEMPT TO FIX COLOR CHANGE)
def normalize_image_colors(images):
    normalized_images = []
    for img in images:
        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(img_lab)
        l = cv2.equalizeHist(l)
        img_lab = cv2.merge((l, a, b))
        img_bgr = cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)
        normalized_images.append(img_bgr)
    return normalized_images

def stitch_images(images):
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        raise Exception("Error during stitching process")
    return stitched

# Conditionally handle the GPS based on platform
def get_real_time_gps():
    if platform.system() == "Windows":
        print("Real-time GPS is not supported on Windows. Using mock GPS data.")
        return 47.6062, -122.3321, 0.0  # Mock data (Seattle, WA)
    else:
        gps_handler = GPSHandler('')
        gps_data = gps_handler.get_real_time_gps()
        if gps_data:
            return gps_data
        else:
            raise Exception("Failed to retrieve real-time GPS data")

if len(sys.argv) != 2:
    print("Usage: python script-v2.py <Image folder path>")
    sys.exit(1)

path = sys.argv[1]
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

# load images
images = [cv2.imread(f) for f in files]

# normalize image colors (for color change fix)
normalized_images = normalize_image_colors(images)

# stitch images and save pano
panorama = stitch_images(normalized_images)
panorama_path = os.path.join(path, "panorama.jpg")
cv2.imwrite(panorama_path, panorama)

# save a PIL version for further processing, if needed
panorama_pil = Image.fromarray(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
panorama_pil.save(os.path.join(path, "panorama_pil.jpg"))

# process GPS coordinates
try:
    lat, lng, alt = get_real_time_gps()
    print(f"Obtained GPS coordinates: {lat}° N, {lng}° W")
except Exception as e:
    print(f"Error retrieving GPS coordinates: {e}")
    sys.exit(1)

# use GPSHandler to read/write and then overlay the data on pano
gps_handler = GPSHandler(panorama_path)
gps_handler.write_gps(lat, lng, alt)        # write to image
gps_data = gps_handler.read_gps()           # read gps back from the image (check formatting)
if gps_data:
    print(f"Read GPS data: {gps_data}")

# overlay the GPS data on pano
newpath = gps_handler.overlay_gps((lat, lng, alt))  # data should be a tuple
if newpath:
    print(f"Panorama with GPS overlay saved as: {newpath}")
else:
    print("Failed to overlay GPS data on the panorama image.")
