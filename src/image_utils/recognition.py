# src/image_utils/recognition.py

from transformers import AutoProcessor, AutoModelForImageClassification
from PIL import Image
import torch

class ImageRecognition:
    def __init__(self, model_name="google/vit-base-patch16-224", device=None):
        """
        A general image classification model using Vision Transformer (ViT)
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name).to(self.device)
        self.labels = self.model.config.id2label  # maps class index → label

    def predict(self, image_path: str):
        """Predicts the top label and probability."""
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            top_prob, top_idx = torch.max(probs, dim=-1)

        label = self.labels[int(top_idx)]
        return label, float(top_prob)
