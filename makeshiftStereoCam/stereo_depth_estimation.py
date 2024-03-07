# Perry Chien, Husky Robotics, PY 2024
# Last updated 3/7/24

# This method handles the depth estimation of the makeshift stereo camera
# (STEP 2). This part of the workflow utilizes a triangulation algo that
# takes in two snapshot views of the same object, taken from the same y-
# and z- object distances. The only variation comes in the form of the x-
# distances, which is inflicted by positioning the lens (i.e. camera) a
# set x-distance between snapshot location 1 and 2. This algorithm follows
# the exact logic used for industry-standard stereo cameras.

import numpy as np
import cv2 as cv
import glob

# Load calibration parameters
with np.load('calibration_params.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

# Define relative distance between virtual cameras
baseline = 0.2  # 20 cm in x-direction

# Load left and right images (here we simulate as two views from the same camera displaced horizontally)
img_left = cv.imread('left_image.jpg')
img_right = cv.imread('right_image.jpg')

# Undistort images
img_left_undistorted = cv.undistort(img_left, mtx, dist, None, mtx)
img_right_undistorted = cv.undistort(img_right, mtx, dist, None, mtx)

# Compute disparity map
stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(cv.cvtColor(img_left_undistorted, cv.COLOR_BGR2GRAY),
                           cv.cvtColor(img_right_undistorted, cv.COLOR_BGR2GRAY))

# Compute depth map
depth_map = np.zeros_like(disparity, dtype=np.float32)
for y in range(depth_map.shape[0]):
    for x in range(depth_map.shape[1]):
        depth_map[y, x] = baseline * mtx[0, 0] / disparity[y, x]

# Find depth at the center (average of left and right disparity values)
center_x = depth_map.shape[1] // 2
center_depth = (depth_map[:, center_x - 1] + depth_map[:, center_x]) / 2
average_depth = np.mean(center_depth)

print("Estimated depth at center location:", average_depth, "meters")