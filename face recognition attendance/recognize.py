
import cv2
from mysql_attendance import mark_attendance


# Student ID -> Student Name
student_names = {
    1: "Shagun Yadav"
}


# Load trained face recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")


# Load face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Start camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


print("Starting face recognition...")
print("Press Q to quit.")


while True:

    # Read camera frame
    success, frame = camera.read()

    if not success:
        print("Could not access camera")
        break


    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Detect faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )


    # Process every detected face
    for (x, y, w, h) in faces:

        # Predict student ID
        student_id, confidence = recognizer.predict(
            gray[y:y+h, x:x+w]
        )


        # Check recognition confidence
        if confidence < 100:

            # Get student name
            student_name = student_names.get(
                student_id,
                f"Student {student_id}"
            )

            name = student_name


            # Mark attendance
            mark_attendance(student_id)

        else:

            name = "Unknown"


        # Draw rectangle around face
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )


        # Display name
        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Display recognition distance
        cv2.putText(
            frame,
            f"Distance: {confidence:.1f}",
            (x, y + h + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


    # Display camera window
    cv2.imshow(
        "Face Recognition Attendance",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release camera
camera.release()
cv2.destroyAllWindows()
 

