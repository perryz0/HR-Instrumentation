# Perry Chien, Husky Robotics, PY 2024
# Last updated 3/7/24

# This method handles the camera calibration part of the makeshift stereo
# camera (STEP 1). This part of the workflow is used to find the distortion
# parameters of the Mastcam module. Once calibrated using an algorithm that
# looks for known object and image points (i.e. chessboard corners), these
# calibration parameters can be fed into STEP 2, the triangulation algo to
# estimate depth using two views captured by the single Mastcam.

import numpy as np
import cv2 as cv
import glob

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# new glob
images = glob.glob('*.jpg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (7,6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
cv.destroyAllWindows()

# Calibration using the generated objpoints and imgpoints
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save the calibration results
np.savez('camera_calib.npz', camera_matrix=mtx, dist_coeffs=dist)

print("Camera calibration parameters saved to 'camera_calib.npz'.")