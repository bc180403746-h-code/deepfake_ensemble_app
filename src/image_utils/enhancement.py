import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os


def enhance_image_cv2(image_path, output_path=None):
    """Apply sharpening and histogram equalization using OpenCV + PIL fallback."""
    image_path = os.path.abspath(image_path)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at: {image_path}")

    img = cv2.imread(image_path)

    # Fallback: use PIL if OpenCV can't decode
    if img is None:
        try:
            pil_img = Image.open(image_path).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception:
            raise ValueError(f"Failed to load image (possibly corrupted or unsupported): {image_path}")

    # Convert to gray for histogram equalization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eq_gray = cv2.equalizeHist(gray)
    img[:, :, 0] = eq_gray
    img[:, :, 1] = eq_gray
    img[:, :, 2] = eq_gray

    # Sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharp_img = cv2.filter2D(img, -1, kernel)

    if output_path:
        output_path = os.path.abspath(output_path)
        cv2.imwrite(output_path, sharp_img)

    return sharp_img


def enhance_image_pil(image_path, output_path=None, factor=1.5):
    """Enhance contrast using PIL."""
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    enhanced_img = enhancer.enhance(factor)

    if output_path:
        enhanced_img.save(output_path)
    return enhanced_img
