import cv2
import os

# Create dataset folder if it doesn't exist
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Ask for student ID
student_id = input("Enter student ID: ")

# Load face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Open webcam
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

count = 0

print("Starting face capture...")
print("Look at the camera.")
print("Press Q to stop.")

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        count += 1

        # Save face image
        filename = f"dataset/User.{student_id}.{count}.jpg"

        cv2.imwrite(filename, gray[y:y+h, x:x+w])

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Images: {count}/30",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Register Student", frame)

    key = cv2.waitKey(100) & 0xFF

    if key == ord("q"):
        break

    if count >= 30:
        break

print("Face capture completed!")
print(f"Total images saved: {count}")

camera.release()
cv2.destroyAllWindows()