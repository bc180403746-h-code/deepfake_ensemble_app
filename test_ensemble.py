# test_ensemble.py

from src.ensemble.ensemble_core import DeepfakeEnsemble
from src.image_utils.enhancement import enhance_image_cv2
import cv2

# --- Step 1: define input paths ---
image_path = "data/samples/sample_image.jpg"
video_path = "data/samples/sample_video.mp4"

# --- Step 2: enhance image before ensemble prediction (for debugging/visual check) ---
enhanced_preview_path = "data/samples/enhanced_preview.jpg"
enhanced_img = enhance_image_cv2(image_path, enhanced_preview_path)
print("✅ Image enhancement applied successfully!")

# Optional: visualize enhancement in OpenCV window (can skip if headless)
# cv2.imshow("Enhanced Image", enhanced_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# --- Step 3: initialize ensemble (image + video only for now) ---
ensemble = DeepfakeEnsemble(weights=(0.4, 0.6, 0.0))

# --- Step 4: run prediction ---
label, probs = ensemble.predict(image_path=image_path, video_path=video_path)

# --- Step 5: display results ---
print("✅ Image enhancement + Deepfake Prediction Complete!")
print(f"Prediction: {label}")
print(f"Probabilities: Real={probs[0]:.4f}, Fake={probs[1]:.4f}")
