# image_capture.py
# Perry Chien, Husky Robotics, PY 2024
# Handles image capture for simulated stereo vision using a single camera.

import cv2 as cv
import time

def capture_images(camera_index=0, delay=1, save_path='captures/'):
    # Captures two images with a single camera, simulating stereo vision.
    # Parameters:
    # - camera_index: The index of the camera device.
    # - delay: Time in seconds to wait before capturing the second image.
    # - save_path: Directory where captured images will be saved.
    # Returns:
    # - img_left: First captured image.
    # - img_right: Second captured image.
    
    camera = cv.VideoCapture(camera_index)
    ret, img_left = camera.read()
    if not ret:
        print("Failed to capture the first image.")
        camera.release()
        return None, None

    cv.imwrite(f'{save_path}left_image.jpg', img_left)
    time.sleep(delay)
    ret, img_right = camera.read()
    if not ret:
        print("Failed to capture the second image.")
        camera.release()
        return None, None

    cv.imwrite(f'{save_path}right_image.jpg', img_right)
    camera.release()
    return img_left, img_right
