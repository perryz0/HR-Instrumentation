# stereo_depth_estimation.py
# Perry Chien, Husky Robotics, PY 2024
# Computes depth using the simulated stereo vision setup.

import cv2 as cv
import numpy as np

def compute_depth(left_image_path, right_image_path, baseline=0.2, calibration_params='calibration_params.npz'):
    # Computes the depth map using the simulated stereo vision images.
    # Parameters:
    # - left_image_path: Path to the left image.
    # - right_image_path: Path to the right image.
    # - baseline: The distance between the two virtual camera positions.
    # - calibration_params: File path to saved camera calibration parameters.
    # Returns:
    # - depth_map: The computed depth map.
    # - average_depth: Estimated average depth at the center.
    
    with np.load(calibration_params) as X:
        mtx, dist = [X[i] for i in ('mtx', 'dist')]

    img_left = cv.imread(left_image_path)
    img_right = cv.imread(right_image_path)
    img_left_undistorted = cv.undistort(img_left, mtx, dist, None, mtx)
    img_right_undistorted = cv.undistort(img_right, mtx, dist, None, mtx)

    stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(cv.cvtColor(img_left_undistorted, cv.COLOR_BGR2GRAY),
                               cv.cvtColor(img_right_undistorted, cv.COLOR_BGR2GRAY))

    depth_map = np.zeros_like(disparity, dtype=np.float32)
    for y in range(depth_map.shape[0]):
        for x in range(depth_map.shape[1]):
            if disparity[y, x] > 0:  # Avoid division by zero
                depth_map[y, x] = baseline * mtx[0, 0] / disparity[y, x]

    center_x = depth_map.shape[1] // 2
    center_depth = (depth_map[:, center_x - 1] + depth_map[:, center_x]) / 2
    average_depth = np.mean(center_depth)

    return depth_map, average_depth
