import cv2
import os
import numpy as np
from PIL import Image


dataset_path = "dataset"
trainer_path = "trainer/trainer.yml"


# Create trainer folder if it doesn't exist
if not os.path.exists("trainer"):
    os.makedirs("trainer")


# Face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()


face_samples = []
ids = []


print("Starting model training...")


# Read all images from dataset
for filename in os.listdir(dataset_path):

    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(dataset_path, filename)

    image = Image.open(image_path).convert("L")

    image_numpy = np.array(image, "uint8")


    # Extract Student ID from filename
    # Example: User.1.1.jpg
    parts = filename.split(".")

    if len(parts) < 3:
        continue

    student_id = int(parts[1])


    faces = face_detector.detectMultiScale(
        image_numpy
    )


    for (x, y, w, h) in faces:

        face_samples.append(
            image_numpy[y:y+h, x:x+w]
        )

        ids.append(student_id)


print(f"Training on {len(face_samples)} face samples...")


if len(face_samples) == 0:

    print("No face samples found.")
    print("Please capture student faces first.")

else:

    recognizer.train(
        face_samples,
        np.array(ids)
    )

    recognizer.write(trainer_path)

    print("Model training completed successfully!")
    print(f"Model saved to: {trainer_path}")