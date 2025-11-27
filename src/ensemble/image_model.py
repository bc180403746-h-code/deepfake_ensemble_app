# src/ensemble/image_model.py
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
from src.image_utils.enhancement import enhance_image_cv2
import cv2
import os

import torch

class ImageDeepfakeModel:
    def __init__(self, model_name="prithivMLmods/deepfake-detector-model-v1", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load image model and processor (no tokenizer)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)
        try:
            # Try standard image processor first
            self.processor = AutoImageProcessor.from_pretrained(model_name)
        except Exception:
            # Fallback for incomplete configs
            print("⚠️ Using fallback processor (ViT-based defaults)...")
            self.processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")

    def predict(self, image_path: str):
        # 1️⃣ Enhance the image first
        enhanced_path = "data/samples/enhanced_temp.jpg"
        enhanced_img = enhance_image_cv2(image_path, enhanced_path)

        # 2️⃣ Reload the enhanced image
        image = Image.open(enhanced_path).convert("RGB")

        # 3️⃣ Continue with normal processing
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
          outputs = self.model(**inputs)
          probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()[0]

        # 4️⃣ Optional cleanup
        if os.path.exists(enhanced_path):
           os.remove(enhanced_path)

        return probs

