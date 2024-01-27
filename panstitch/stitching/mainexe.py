# Adam Friesz, Husky Robotics, PY 2024
# Last updated 1/20/24

# This method stitches together images in the image folder to create a panorama. 
# The panorama will be saved in the same folder as the images and named panorama.jpeg
# This program should be run from the terminal and stored in the correct directory hierarchy
# for everything to run correctly. Do not change the organization of the folders after unzipping.

from stitching import Stitcher # Open Stitching uses OpenCV to create panorama
import os # os allows us to read the file names inside our selected folder
from PIL import Image # pillow allows us to turn the numpy.array that OpenStitching creates into a jpg

path = input("Image folder path: ")
files = []

for entry in os.listdir(path):
    pentry = path + "/" + entry
    try:
        Image.open(pentry)
        files.append(pentry)
    except IOError: # if entry is not a recognized image file Image.open() returns an IOError.
        print(entry, "is not an image and was skipped.")

if not files: # if files is empty/null
    raise Exception("There are no images to stitch.")

stitcher = Stitcher()
panorama = stitcher.stitch(files)

im = Image.fromarray(panorama)
im.save(path + "/panorama.jpeg")