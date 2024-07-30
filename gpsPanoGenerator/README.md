# GPS Panorama Generator

This script helps to generate a streamlined panorama of rover images alongside indicated GPS coordinates. Customized specifically for the 2023-24 Husky Robotics team, competing in CIRC 2024 taking place in Drumheller, BC, Canada.

## Current progress

There are currently 3 versions of the script:
- script.py: Most basic pano script, possible color-change bugs (and potentially others too)
- script-v2.py: Similar to the most basic, but addressing color-change issue with color normalization
- script-calib.py: Does exactly what script-v2 does, but must be ran after calibration.py (extracts cam calib params)
    - *Camera calibration is the process of extracting distortion params for a camera with lens distortion, learn more from [OpenCV](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)*


If you are currently testing/refining this GPS Pano Generator script, please use version control and ask @1verd on Discord for Github access (ask anything related to this too). Thanks!