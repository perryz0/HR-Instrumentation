# Perry Chien
#
# Stitching script WITH cam calibration (refined ver. of script-v2)
#
# WIP refined version of the stitching script. Trying to address the color change issue
# (i.e. yellowish to blueish for no reason). This ver is compatible with newly calibrated
# cam (i.e. takes distortion params)

import sys
import cv2
import numpy as np
import os
import numba
from PIL import Image
from overlay import overlayText
from imgdata import set_gps_location, get_gps_location
from matplotlib import pyplot as plt
from gps_handler import GPSHandler

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

def get_real_time_gps():
    # placeholder function to fetch real-time GPS coordinates.
    # replace with actual implementation of WebSocket communication stuff to get GPS data.
    return (47.6062, -122.3321, 15.0)

if len(sys.argv) != 2:
    print("Usage: python script-v2.py <Image folder path>")
    sys.exit(1)

path = sys.argv[1]
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]



# EXTRA CAMERA CALIBRATION STEP
# load calibration data
calibration_data = np.load('camera_calib.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

# load each image and calibrate each one based on the data
images = []
for f in files:
    img = cv2.imread(f)
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]
    images.append(undistorted_img)



# EVERYTHING IS SAME HERE AS SCRIPT-V2.PY
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
lat, lng, alt = get_real_time_gps()
print(f"Obtained GPS coordinates: {lat}° N, {lng}° W")

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