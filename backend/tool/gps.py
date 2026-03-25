"""
GPS Tool
--------
Extracts latitude & longitude from:
1. EXIF metadata
2. OCR text (fallback)
"""

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pytesseract
import cv2
import re


def _convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)


def extract_gps(image_path: str):
    try:
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        # Crop bottom area
        crop = img[int(h * 0.6):h, 0:w]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)

        print("OCR TEXT:\n", text)  # DEBUG

        # -------------------------
        # Extract LAT/LON
        # -------------------------
        lat_match = re.search(r'Lat\s*([\d.]+)', text)
        lon_match = re.search(r'Long\s*([\d.]+)', text)

        lat = float(lat_match.group(1)) if lat_match else None
        lon = float(lon_match.group(1)) if lon_match else None

        # -------------------------
        # Extract LOCATION NAME
        # -------------------------
        location_match = re.search(
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+,\s*India)',
            text
        )

        location_name = location_match.group(1).strip() if location_match else "Unknown Location"

        return lat, lon, location_name

    except Exception as e:
        print("OCR error:", e)
        return None, None, "Unknown Location"