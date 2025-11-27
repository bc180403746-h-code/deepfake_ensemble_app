# test_number_plate_recognition.py

from src.image_utils.number_plate_recognition import NumberPlateRecognizer

image_path = "data/samples/sample_car.jpg"  # <-- Add a car image with a visible number plate

recognizer = NumberPlateRecognizer()
plate_text = recognizer.read_plate_text(image_path)

print("✅ Number Plate Recognition Complete!")
print(f"Detected Plate Text: {plate_text}")
