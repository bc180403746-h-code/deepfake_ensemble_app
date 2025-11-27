# src/ensemble/ensemble_core.py

from .image_model import ImageDeepfakeModel
from .video_model import VideoDeepfakeModel
from .audio_model import AudioDeepfakeModel
from src.image_utils.enhancement import enhance_image_cv2


# optionally save: cv2.imwrite("enhanced.jpg", enhanced_img)
# then pass enhanced image to detector

import numpy as np

class DeepfakeEnsemble:
    def __init__(self, weights=(0.4, 0.6, 0.0)):
        self.image_model = ImageDeepfakeModel()
        self.video_model = VideoDeepfakeModel()
        self.audio_model = AudioDeepfakeModel()
        self.weights = weights  # (image, video, audio)

    def predict(self, image_path=None, video_path=None, audio_path=None):
        results = []
        total_weight = 0

        if image_path:
            img_probs = self.image_model.predict(image_path)
            results.append(self.weights[0] * img_probs)
            total_weight += self.weights[0]

        if video_path:
            vid_probs = self.video_model.predict(video_path)
            results.append(self.weights[1] * vid_probs)
            total_weight += self.weights[1]

        if audio_path:
            aud_probs = self.audio_model.predict(audio_path)
            results.append(self.weights[2] * aud_probs)
            total_weight += self.weights[2]

        
        if not results:
            raise ValueError("No inputs provided (need at least an image).")
        
        final_probs = np.sum(results, axis=0) / total_weight
        label = "Fake" if final_probs[1] > final_probs[0] else "Real"

        return label, final_probs
