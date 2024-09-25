# main.py
# Perry Chien, Husky Robotics, PY 2024
# Main script that integrates calibration, image capture, and depth estimation.

from src.cam_calibration import calibrate_camera
from src.stereo_depth_estimation import compute_depth
from src.image_capture import capture_images

def main():
    # Coordinates the entire process from calibration to depth estimation.
    
    if input("Run camera calibration? (yes/no): ").strip().lower() == 'yes':
        calibrate_camera()

    img_left, img_right = capture_images()
    if img_left is None or img_right is None:
        print("Error in capturing images. Exiting...")
        return

    depth_map, average_depth = compute_depth('captures/left_image.jpg', 'captures/right_image.jpg')
    print(f"Estimated depth at center location: {average_depth:.2f} meters")

if __name__ == "__main__":
    main()
