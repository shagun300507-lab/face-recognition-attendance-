import cv2
import os
import sys

# Check Student ID
if len(sys.argv) < 2:
    print("Please provide Student ID.")
    print("Example: python capture_student_faces.py 1")
    sys.exit()

student_id = sys.argv[1]

# Create dataset folder if it doesn't exist
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# Face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Open camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

count = 0

print("Starting face capture...")
print("Look at the camera.")
print("Press Q to stop.")

while True:

    success, frame = camera.read()

    if not success:
        print("Could not access camera.")
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

        face_image = gray[y:y+h, x:x+w]

        filename = f"dataset/User.{student_id}.{count}.jpg"

        cv2.imwrite(filename, face_image)

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

    cv2.imshow("Capture Student Face", frame)

    # Stop after 30 images
    if count >= 30:
        break

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print(f"Face capture completed for Student ID: {student_id}")
print(f"Total images captured: {count}")