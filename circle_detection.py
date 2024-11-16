#Python script to detect a circle of known diameter in a video stream and calculate the frame
#dimensions in inches and the scale in inches per pixel for microscope calibration.
#The frame dimensions are printed based on the dimensions of the the last detected circle.
#dimensions of reference circle are hardcoded in the script and subject to change based on the calibration slides.
#Directions to run: Run the script and place the calibration slide under the microscope.
import cv2
import numpy as np

# Constants
KNOWN_DIAMETER_MICROMETERS = 3000  # Known diameter of the circle in micrometers
MICROMETERS_PER_INCH = 25400  # Conversion factor: 1 inch = 25,400 micrometers
frame_dimensions_inches = (0, 0)  # Initialize frame dimensions (width, height) in inches
scale_inches_per_pixel = None  # Initialize scale in inches per pixel

# Open video stream (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Function to convert micrometers to inches
def um_to_inches(micrometers):
    return micrometers / MICROMETERS_PER_INCH

# Function to calculate frame dimensions in inches
def calculate_frame_dimensions(frame, detected_diameter_pixels):
    global scale_inches_per_pixel, frame_dimensions_inches
    
    # Calculate the scale in inches per pixel
    scale_um_per_pixel = KNOWN_DIAMETER_MICROMETERS / detected_diameter_pixels
    scale_inches_per_pixel = scale_um_per_pixel / MICROMETERS_PER_INCH
    
    # Get the frame dimensions in pixels
    frame_height, frame_width = frame.shape[:2]
    
    # Calculate frame dimensions in inches
    frame_width_inches = frame_width * scale_inches_per_pixel
    frame_height_inches = frame_height * scale_inches_per_pixel
    
    # Store the frame dimensions
    frame_dimensions_inches = (round(frame_width_inches, 4), round(frame_height_inches, 4))

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
        cv2.circle(frame, center, 2, (0, 0, 255), 3)  # Red center point
    
    # Display the frame dimensions in inches
    cv2.putText(frame, f"Frame Size: {frame_dimensions_inches[0]:.4f}\" x {frame_dimensions_inches[1]:.4f}\"",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Display the scale in inches per pixel if calculated
    if scale_inches_per_pixel is not None:
        cv2.putText(frame, f"Scale: {scale_inches_per_pixel:.6f} inches/pixel", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow("Microscope Calibration with Scale (inches)", frame)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
