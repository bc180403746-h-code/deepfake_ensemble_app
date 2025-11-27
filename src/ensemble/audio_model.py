# src/ensemble/audio_model.py

from transformers import AutoProcessor, AutoModelForAudioClassification
import torch
import numpy as np
import librosa

class AudioDeepfakeModel:
    def __init__(self, model_name="facebook/wav2vec2-base", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForAudioClassification.from_pretrained(model_name).to(self.device)

    def load_audio(self, audio_path, sr=16000):
        """Load audio file as waveform"""
        waveform, _ = librosa.load(audio_path, sr=sr)
        return waveform

    def predict(self, audio_path: str):
        """Predict real/fake probabilities"""
        waveform = self.load_audio(audio_path)
        inputs = self.processor(waveform, sampling_rate=16000, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]

        # If the model has >2 classes, compress to [Real, Fake]-like format for ensemble
        if len(probs) >= 2:
            return np.array([probs[0], probs[1]])
        else:
            return np.array([1 - probs[0], probs[0]])
