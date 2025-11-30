# ensemble_loader.py
import torch
from transformers import (
    AutoProcessor, AutoModelForImageClassification,
    AutoModel, AutoTokenizer, CLIPProcessor, CLIPModel
)
from PIL import Image
import numpy as np

# ------------------------------------------------------------
# 1️⃣  EfficientViT Model
# ------------------------------------------------------------
def load_efficientvit():
    model_id = "Wvolf/ViT_Deepfake_Detection"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForImageClassification.from_pretrained(model_id)
    return processor, model

# ------------------------------------------------------------
# 2️⃣  CLIP-based Multimodal Detector
# ------------------------------------------------------------
def load_clip_detector():
    model_id = "openai/clip-vit-base-patch16"
    processor = CLIPProcessor.from_pretrained(model_id)
    model = CLIPModel.from_pretrained(model_id)
    return processor, model

# ------------------------------------------------------------
# 3️⃣  XceptionNet++ (Hugging Face Deepfake Model)
# ------------------------------------------------------------
def load_xception():
    model_id = "prithivMLmods/Deep-Fake-Detector-v2-Model"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForImageClassification.from_pretrained(model_id)
    return processor, model

# ------------------------------------------------------------
# 4️⃣  (Optional) FakeAVCeleb Audio-Visual Placeholder
# ------------------------------------------------------------
def load_fakeavceleb():
    # If you later integrate audio, handle here (currently placeholder)
    return None, None


# ============================================================
# ENSEMBLE INITIALIZATION
# ============================================================
def init_ensemble(device=None):
    """Load all ensemble models with processors and return dictionary."""
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    eff_proc, eff_model = load_efficientvit()
    clip_proc, clip_model = load_clip_detector()
    xcep_proc, xcep_model = load_xception()

    eff_model.to(device)
    clip_model.to(device)
    xcep_model.to(device)

    return {
        "device": device,
        "efficientvit": (eff_proc, eff_model),
        "clip": (clip_proc, clip_model),
        "xception": (xcep_proc, xcep_model)
    }

# ============================================================
# ENSEMBLE PREDICTION FUNCTION
# ============================================================
def predict_deepfake(image_path, ensemble, weights=(0.3, 0.3, 0.4)):
    """Combine predictions from EfficientViT, CLIP, and Xception++"""
    device = ensemble["device"]
    image = Image.open(image_path).convert("RGB")

    scores = []

    # EfficientViT
    proc, model = ensemble["efficientvit"]
    inputs = proc(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    score_eff = torch.softmax(outputs.logits, dim=-1)[0, 1].item()
    scores.append(score_eff)

    # CLIP
    proc, model = ensemble["clip"]
    clip_inputs = proc(text=["a real face", "a fake face"], images=image, return_tensors="pt", padding=True).to(device)
    clip_outputs = model(**clip_inputs)
    logits_per_image = clip_outputs.logits_per_image.softmax(dim=-1)
    score_clip = logits_per_image[0, 1].item()
    scores.append(score_clip)

    # Xception++
    proc, model = ensemble["xception"]
    inputs = proc(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    score_xcep = torch.softmax(outputs.logits, dim=-1)[0, 1].item()
    scores.append(score_xcep)

    # Weighted ensemble average
    final_score = np.average(scores, weights=weights)
    label = "FAKE" if final_score > 0.5 else "REAL"

    return {
        "score": final_score,
        "label": label,
        "sub_scores": {
            "EfficientViT": score_eff,
            "CLIP": score_clip,
            "Xception++": score_xcep
        }
    }



#download sample image automatically

import requests
from PIL import Image

def download_sample_image():
    url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/cat.png"
    os.makedirs("samples", exist_ok=True)
    image_path = "samples/sample.jpg"
    Image.open(requests.get(url, stream=True).raw).convert("RGB").save(image_path)
    return image_path

if __name__ == "__main__":
    image_path = download_sample_image()
    ensemble = init_ensemble()
    result = predict_deepfake(image_path, ensemble)
    print(result)
