from utils.database_manager import (
    add_student,
    student_exists
)
from utils.face_encoder import encode_student
from utils.database_manager import add_student
import cv2
from pathlib import Path
from utils.face_detector import detect_faces


def create_student_folder(name, roll_number):
    """
    Creates a folder for the student inside the images directory.
    """

    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)

    student_folder = images_dir / f"{name}_{roll_number}"
    student_folder.mkdir(exist_ok=True)

    return student_folder


def start_registration(name, roll):
    """
    Registers a student using the supplied name and roll number.
    """

    student_folder = create_student_folder(name, roll)

    print(f"\nFolder Created: {student_folder}")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return False

    count = 0

    print("\nMove your face slightly while images are being captured...")

    while True:

        success, frame = camera.read()

        if not success:
            break

        faces = detect_faces(frame)

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

            face = frame[y:y+h, x:x+w]

            filename = student_folder / f"image_{count+1}.jpg"

            cv2.imwrite(str(filename), face)

            count += 1

            cv2.putText(
                frame,
                f"Captured : {count}/30",
                (10,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            cv2.waitKey(150)

            if count >= 30:

                camera.release()
                cv2.destroyAllWindows()

                return True

        cv2.imshow("Student Registration", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):

            camera.release()
            cv2.destroyAllWindows()

            return False

if __name__ == "__main__":

    name = input("Enter Student Name: ")
    roll = input("Enter Roll Number: ")

    start_registration(name, roll)