# src/image_utils/number_plate_recognition.py

import cv2
import easyocr
import numpy as np
import re
from PIL import Image

class NumberPlateRecognizer:
    def __init__(self):
        """Initialize EasyOCR reader for English plates."""
        self.reader = easyocr.Reader(['en'])

    def detect_plate_region(self, image_path):
        """Detect rectangular region that looks like a plate, with safe image loading."""
        try:
            # Try reading with OpenCV first
            img = cv2.imread(image_path)
            if img is None:
                # Fallback: use Pillow (handles JPG/PNG/WEBP better)
                pil_img = Image.open(image_path).convert("RGB")
                img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise FileNotFoundError(f"❌ Cannot open image: {image_path} — {e}")

        if img is None:
            raise FileNotFoundError(f"❌ Image not found or unreadable: {image_path}")

        # Convert to grayscale and find edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blur, 30, 200)

        # Find contours and pick rectangular regions
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        plate_region = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:  # looks like rectangle
                x, y, w, h = cv2.boundingRect(contour)
                plate_region = img[y:y+h, x:x+w]
                break

        return plate_region

    def read_plate_text(self, image_path):
        """Run OCR on detected plate region and extract text."""
        plate_img = self.detect_plate_region(image_path)
        if plate_img is None:
            return "No plate detected"

        result = self.reader.readtext(plate_img)
        if not result:
            return "Text not detected"

        # Extract likely plate text (letters/numbers only)
        texts = [r[1] for r in result if re.match(r'^[A-Z0-9-]+$', r[1].upper())]
        return texts[0] if texts else result[0][1]
