# test_image_recognition.py

from src.image_utils.recognition import ImageRecognition

image_path = "data/samples/sample_image.jpg"

recognizer = ImageRecognition()
label, prob = recognizer.predict(image_path)

print("✅ Image Recognition Complete!")
print(f"Predicted Label: {label}")
print(f"Confidence: {prob:.4f}")
