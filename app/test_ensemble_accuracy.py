# test_ensemble_accuracy.py
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tqdm import tqdm
from ensemble_loader import init_ensemble, predict_deepfake
from PIL import Image
import requests

# ------------------------------------------------------------
# STEP 1 — Load ensemble
# ------------------------------------------------------------
ensemble = init_ensemble()

# ------------------------------------------------------------
# STEP 2 — Sample image set (you can later replace with dataset)
# ------------------------------------------------------------
os.makedirs("samples_test", exist_ok=True)

# Download small demo dataset (2 real + 2 fake)
sample_images = {
    "real1.jpg": "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png",
    "real2.jpg": "https://upload.wikimedia.org/wikipedia/commons/3/34/Face_of_a_man.jpg",
    "fake1.jpg": "https://huggingface.co/datasets/prithivMLmods/fakeface-dataset/resolve/main/fakeface_1.jpg",
    "fake2.jpg": "https://huggingface.co/datasets/prithivMLmods/fakeface-dataset/resolve/main/fakeface_2.jpg"
}

for name, url in sample_images.items():
    path = f"samples_test/{name}"
    if not os.path.exists(path):
        Image.open(requests.get(url, stream=True).raw).convert("RGB").save(path)

# Labels: 0 = Real, 1 = Fake
test_data = [
    ("samples_test/real1.jpg", 0),
    ("samples_test/real2.jpg", 0),
    ("samples_test/fake1.jpg", 1),
    ("samples_test/fake2.jpg", 1)
]

# ------------------------------------------------------------
# STEP 3 — Run predictions
# ------------------------------------------------------------
y_true, y_pred, scores = [], [], []

print("🔍 Running ensemble inference...")
for img_path, label in tqdm(test_data):
    result = predict_deepfake(img_path, ensemble)
    y_true.append(label)
    y_pred.append(1 if result["label"] == "FAKE" else 0)
    scores.append(result["score"])

# ------------------------------------------------------------
# STEP 4 — Compute metrics
# ------------------------------------------------------------
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)
cm = confusion_matrix(y_true, y_pred)

# ------------------------------------------------------------
# STEP 5 — Display results
# ------------------------------------------------------------
print("\n🎯 Ensemble Deepfake Detection Results")
print(f"Accuracy:  {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall:    {rec:.3f}")
print(f"F1 Score:  {f1:.3f}")
print(f"Confusion Matrix:\n{cm}")
print(f"\nAverage Score: {np.mean(scores):.3f}")
