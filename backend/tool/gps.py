
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import easyocr
import cv2
import re

# 🔥 Initialize EasyOCR reader (CPU only for Render)
reader = easyocr.Reader(['en'], gpu=False)


def extract_gps(image_path: str):
    try:
        img = cv2.imread(image_path)

        if img is None:
            return None, None, "Unknown Location"

        h, w, _ = img.shape

        # Crop bottom area (where GPS text usually exists)
        crop = img[int(h * 0.6):h, 0:w]

        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # 🔥 EASYOCR (replaces pytesseract)
        results = reader.readtext(gray)

        # Combine detected text
        text = " ".join([res[1] for res in results])

        print("OCR TEXT:\n", text)  # DEBUG

        # -------------------------
        # Extract LAT/LON
        # -------------------------
        lat_match = re.search(r'(Lat|Latitude)[:\s]*([\d.]+)', text)
        lon_match = re.search(r'(Long|Longitude)[:\s]*([\d.]+)', text)

        lat = float(lat_match.group(2)) if lat_match else None
        lon = float(lon_match.group(2)) if lon_match else None

        # -------------------------
        # Extract LOCATION NAME
        # -------------------------
        location_match = re.search(
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+,\s*India)',
            text
        )

        location_name = (
            location_match.group(1).strip()
            if location_match
            else "Unknown Location"
        )

        return lat, lon, location_name

    except Exception as e:
        print("OCR error:", e)
        return None, None, "Unknown Location"
