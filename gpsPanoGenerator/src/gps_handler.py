# Perry Chien
# GPSHandler object that handles reading, writing, and overlaying of 
# GPS coordinates on an image. 

from PIL import Image
from overlay import overlayText
from imgdata import set_gps_location, get_gps_location

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