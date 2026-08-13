import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera.")
    exit()

success, frame = camera.read()

if success:
    print("Type:", type(frame))
    print("Shape:", frame.shape)
    print("Data Type:", frame.dtype)

camera.release()