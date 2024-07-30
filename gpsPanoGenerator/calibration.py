# Perry Chien, Husky Robotics, PY 2024
# Last updated 7/29/24

# This method helps to extract calibration params of a cam module connected
# to the machine, all params are redirected into a new .npz file that can be
# processed by the GPS pano script.

import numpy as np
import cv2 as cv

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# capture images from the camera (real-time compatibility)
cap = cv.VideoCapture(0)  # Use 0 for the default camera, or change it to the appropriate camera index

while True:
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # find chess board corners for calibration
    ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    # if found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # draw and display corners
        cv.drawChessboardCorners(img, (7,6), corners2, ret)
        cv.imshow('img', img)

    # display the frame
    cv.imshow('Frame', img)

    # press Q to break the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

# calibration params using the generated objpoints and imgpoints
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# save the calibration results into .npz file
np.savez('camera_calib.npz', camera_matrix=mtx, dist_coeffs=dist)

print("Camera calibration params saved to 'camera_calib.npz'.")