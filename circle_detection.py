import cv2
import numpy as np

# Constants
KNOWN_DIAMETER_MICROMETERS = 3000  # Known diameter of the circle in micrometers
frame_dimensions_um = (0, 0)  # Initialize frame dimensions (width, height) in micrometers
scale_um_per_pixel = None  # Initialize scale in micrometers per pixel

# Open video stream (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Function to calculate frame dimensions in micrometers
def calculate_frame_dimensions(frame, detected_diameter_pixels):
    global scale_um_per_pixel, frame_dimensions_um
    
    # Calculate the scale in micrometers per pixel
    scale_um_per_pixel = KNOWN_DIAMETER_MICROMETERS / detected_diameter_pixels

    # Get the frame dimensions in pixels
    frame_height, frame_width = frame.shape[:2]

    # Calculate frame dimensions in micrometers
    frame_width_um = frame_width * scale_um_per_pixel
    frame_height_um = frame_height * scale_um_per_pixel

    # Store the frame dimensions
    frame_dimensions_um = (round(frame_width_um, 2), round(frame_height_um, 2))

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)  # Reduce noise

    # Detect circles using Hough Transform
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                               param1=100, param2=30, minRadius=30, maxRadius=100)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # Use the first detected circle
        circle = circles[0, 0]
        radius = circle[2]
        detected_diameter_pixels = 2 * radius
        
        # Update frame dimensions based on new circle detection
        calculate_frame_dimensions(frame, detected_diameter_pixels)
        
        # Draw the detected circle
        center = (circle[0], circle[1])
        cv2.circle(frame, center, radius, (255, 0, 0), 2)  # Blue circle
        cv2.circle(frame, center, 2, (0, 0, 255), 3)       # Red center point

    # Display the frame dimensions in micrometers
    cv2.putText(frame, f"Frame Size: {frame_dimensions_um[0]} um x {frame_dimensions_um[1]} um",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the scale in micrometers per pixel if calculated
    if scale_um_per_pixel is not None:
        cv2.putText(frame, f"Scale: {round(scale_um_per_pixel, 2)} um/pixel", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Microscope Calibration with Scale", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
