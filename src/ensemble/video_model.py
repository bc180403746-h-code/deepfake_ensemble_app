# src/ensemble/video_model.py

from transformers import AutoModelForVideoClassification, AutoProcessor
import cv2
import numpy as np
import torch


class VideoDeepfakeModel:
    def __init__(self, model_name="MCG-NJU/videomae-base-finetuned-kinetics", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForVideoClassification.from_pretrained(model_name).to(self.device)
        self.processor = AutoProcessor.from_pretrained(model_name)

    def extract_frames(self, video_path, frame_skip=15):
        """Extract every Nth frame to reduce processing load."""
        cap = cv2.VideoCapture(video_path)
        frames = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_skip == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
            count += 1
        cap.release()
        return frames

    def predict(self, video_path: str):
        frames = self.extract_frames(video_path)
        if not frames:
            raise ValueError("No frames extracted from video!")

        # Processor expects a single list of frames under key 'video'
        inputs = self.processor(images=list(frames), return_tensors="pt").to(self.device)


        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()[0]

        # Normalize to 2-class [Real, Fake] style output
        if len(probs) >= 2:
            return np.array([probs[0], probs[1]])
        else:
            return np.array([1 - probs[0], probs[0]])

