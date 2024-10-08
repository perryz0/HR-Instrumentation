# Perry Chien
# GPSHandler object that handles reading, writing, and overlaying of 
# GPS coordinates on an image. 

import platform
from PIL import Image
from ..image_processing.overlay import overlayText
from ..image_processing.imgdata import set_gps_location, get_gps_location

# Conditionally import gpsd if not on Windows
if platform.system() != "Windows":
    import gpsd

class GPSHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_gps(self):
        try:
            return get_gps_location(self.filepath)
        except Exception as e:
            print(f"Error reading GPS data: {e}")
            return None

    def write_gps(self, lat, lng, alt):
        try:
            set_gps_location(self.filepath, lat, lng, alt)
            return get_gps_location(self.filepath)
        except Exception as e:
            print(f"Error writing GPS data: {e}")
            return None

    def overlay_gps(self, gps_data):
        try:
            if gps_data and isinstance(gps_data, tuple) and len(gps_data) == 3:
                gps_text = f"{gps_data[0]:.2f}° N, {gps_data[1]:.2f}° W"
                print(f"Overlaying GPS coordinates: {gps_text}")
                newpath = self.filepath[:self.filepath.index('.')] + '-gps.jpg'
                img = Image.open(self.filepath)
                img = overlayText(img, gps_text, 'br')
                img.save(newpath)
                return newpath
            else:
                print("Invalid GPS data format.")
                return None
        except Exception as e:
            print(f"Error overlaying GPS data: {e}")
            return None

    def get_real_time_gps(self):
        """
        If running on Windows, skip this function as gpsd is not available.
        If running on Unix-like OS (Linux/macOS), use gpsd for real-time GPS.
        """
        if platform.system() == "Windows":
            print("Real-time GPS is not supported on Windows. Returning mock data.")
            # Return mock data or skip real-time GPS functionality
            return 47.6062, -122.3321, 0.0  # Mock GPS coordinates (Seattle, WA)
        else:
            try:
                # Connect to the gpsd service running on localhost
                gpsd.connect()

                # Get the latest GPS data packet
                packet = gpsd.get_current()

                # Extract latitude, longitude, and altitude
                latitude = packet.lat
                longitude = packet.lon
                altitude = packet.alt

                # Return the GPS coordinates
                return latitude, longitude, altitude
            except Exception as e:
                print(f"Error fetching GPS data: {e}")
                return None
