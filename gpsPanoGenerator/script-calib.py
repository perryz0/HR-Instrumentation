# Perry Chien
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

numba.config.DISABLE_JIT = True  # Disable Numba JIT caching

def plot_image(img, figsize_in_inches=(5,5)):
    fig, ax = plt.subplots(figsize=figsize_in_inches)
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

# normalize colors across a series of images
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

class GPSHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_gps(self):
        try:
            return get_gps_location(self.filepath)
        except Exception as e:
            print(f"Error reading GPS data: {e}")
            return None

    def write_gps(self, lat, lng, alt):
        try:
            set_gps_location(self.filepath, lat, lng, alt)
            return get_gps_location(self.filepath)
        except Exception as e:
            print(f"Error writing GPS data: {e}")
            return None

    def overlay_gps(self, gps_data):
        try:
            if gps_data and isinstance(gps_data, tuple) and len(gps_data) == 3:
                gps_text = f"{gps_data[0]:.2f}° N, {gps_data[1]:.2f}° W"
                print(f"Overlaying GPS coordinates: {gps_text}")
                newpath = self.filepath[:self.filepath.index('.')] + '-gps.jpg'
                img = Image.open(self.filepath)
                img = overlayText(img, gps_text, 'br')
                img.save(newpath)
                return newpath
            else:
                print("Invalid GPS data format.")
                return None
        except Exception as e:
            print(f"Error overlaying GPS data: {e}")
            return None

if len(sys.argv) != 2:
    print("Usage: python script-v2.py <Image folder path>")
    sys.exit(1)

path = sys.argv[1]
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

# Load calibration data
calibration_data = np.load('camera_calib.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

# Load and undistort images
images = []
for f in files:
    img = cv2.imread(f)
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]
    images.append(undistorted_img)

# Normalize image colors
normalized_images = normalize_image_colors(images)

# Stitch images
panorama = stitch_images(normalized_images)

# Save panorama
panorama_path = os.path.join(path, "panorama.jpg")
cv2.imwrite(panorama_path, panorama)

# Convert to PIL for further processing (optional)
panorama_pil = Image.fromarray(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
panorama_pil.save(os.path.join(path, "panorama_pil.jpg"))

# Obtain real-time GPS coordinates
lat, lng, alt = get_real_time_gps()
print(f"Obtained GPS coordinates: {lat}° N, {lng}° W")

# Create an instance of GPSHandler for the panorama image
gps_handler = GPSHandler(panorama_path)

# Write the GPS data to the image
gps_handler.write_gps(lat, lng, alt)

# Read the GPS data back from the image (ensure correct format)
gps_data = gps_handler.read_gps()
if gps_data:
    print(f"Read GPS data: {gps_data}")

# Overlay the GPS data on the panorama image
newpath = gps_handler.overlay_gps((lat, lng, alt))  # Ensure GPS data is passed as a tuple
if newpath:
    print(f"Panorama with GPS overlay saved as: {newpath}")
else:
    print("Failed to overlay GPS data on the panorama image.")