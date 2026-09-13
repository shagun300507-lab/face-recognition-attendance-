import cv2

print("OpenCV version:", cv2.__version__)

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera opened:", camera.isOpened())

while True:
    success, frame = camera.read()

    print("Frame:", success, "Size:", frame.shape if success else "None")

    if not success:
        break

    cv2.imshow("Webcam Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()