import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import requests

# ------------------------------
# MODEL: prithivMLmods/deepfake-detector-model-v1
# ------------------------------

MODEL_NAME = "prithivMLmods/deepfake-detector-model-v1"

# Load processor and model
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

# Optional: Test image (you can replace with your own file path)
url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/cats.png"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")  # ensure 3-channel RGB

# Preprocess (fix: wrap image in list)
inputs = processor(images=[image], return_tensors="pt")

# Inference
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    preds = torch.nn.functional.softmax(logits, dim=-1)
    pred_id = preds.argmax(-1).item()
    confidence = preds[0, pred_id].item() * 100

# Results
label = model.config.id2label[pred_id]
print(f"Prediction: {label} ({confidence:.2f}%)")
