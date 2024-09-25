# cam_calibration.py
# Perry Chien, Husky Robotics, PY 2024
# Performs camera calibration to obtain distortion parameters.

import cv2 as cv
import numpy as np
import glob

def calibrate_camera(save_path='calibration_params.npz'):
    # Calibrates the camera and saves calibration parameters.
    # Saves the camera intrinsic parameters and distortion coefficients.
    
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    images = glob.glob('*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, (7,6), None)
        if ret:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            cv.drawChessboardCorners(img, (7,6), corners2, ret)
            cv.imshow('img', img)
            cv.waitKey(500)
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez(save_path, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    print(f"Calibration parameters saved to {save_path}")
