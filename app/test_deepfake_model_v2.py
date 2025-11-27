import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import requests

MODEL_NAME = "prithivMLmods/Deep-Fake-Detector-v2-Model"

# Load model & processor
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

# Test image (replace URL or use local file)
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/cats.png"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Preprocess
inputs = processor(images=[image], return_tensors="pt")

# Inference
with torch.no_grad():
    outputs = model(**inputs)
    preds = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred_id = preds.argmax(-1).item()
    confidence = preds[0, pred_id].item() * 100

label = model.config.id2label[pred_id]
print(f"[v2 MODEL] Prediction: {label} ({confidence:.2f}%)")
