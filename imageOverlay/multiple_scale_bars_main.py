# Perry Chien, Husky Robotics
# Last Updated 3/7/24

# This class implements functions from overlay to implement scale bars and
# numpy & cv2 to perform elementary depth estimations. The desired output
# is a three-layered scale bar that is optimally placed at the foreground,
# middle ground, and background.
# 
# 
# ***The depth_estimation algo is not working properly yet and next steps
# would be to settle on more precise determinants as to what is classified
# "fg", "mg", and "bg"***

import cv2
import numpy as np
from overlay import overlayScalebar
from PIL import Image

# CURRENTLY PROBLEMATIC. NEEDS FIX_V2.
def depth_estimation(image):
    # Perform depth estimation using OpenCV method
    # Replace this with your preferred depth estimation method
    depth_map = np.zeros_like(image)
    # Placeholder: for demonstration purposes, we assume the depth map is a grayscale image
    depth_map = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)
    return depth_map

def generate_scalebar(image, depth_map):
    # Split the image into foreground, middle ground, and background based on depth map
    # Replace this with your method of segmenting the image based on depth information
    foreground = image.copy()
    middle_ground = image.copy()
    background = image.copy()

    # Generate scale bars for each region
    scalebar_foreground = overlayScalebar(Image.fromarray(foreground), 'br', color=(255, 0, 0))
    scalebar_middle_ground = overlayScalebar(Image.fromarray(middle_ground), 'br', color=(0, 255, 0))
    scalebar_background = overlayScalebar(Image.fromarray(background), 'br', color=(0, 0, 255))

    return scalebar_foreground, scalebar_middle_ground, scalebar_background

def main():
    print("This program generates scale bars for foreground, middle ground, and background of an image.")

    # Load the image
    filepath = input("Enter the filepath of the image: ")
    image = cv2.imread(filepath)

    # Perform depth estimation
    depth_map = depth_estimation(image)

    # Generate scale bars for each region
    scalebar_foreground, scalebar_middle_ground, scalebar_background = generate_scalebar(image, depth_map)

    # Save the images with scale bars
    scalebar_foreground.save(filepath[: filepath.index('.')] + '-scalebar_foreground.jpg')
    scalebar_middle_ground.save(filepath[: filepath.index('.')] + '-scalebar_middle_ground.jpg')
    scalebar_background.save(filepath[: filepath.index('.')] + '-scalebar_background.jpg')

    print("Scale bars generated and saved successfully.")

if __name__ == "__main__":
    main()
