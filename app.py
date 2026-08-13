import cv2
from insightface.app import FaceAnalysis

from utils.database_manager import mark_attendance
from utils.recognizer import (
    load_known_faces,
    recognize_face
)
from utils.database_manager import get_student_id

# ----------------------------------------
# Load AI Model
# ----------------------------------------
def start_attendance():
    """
    Starts the AI attendance system.
    """
    print("Loading AI Model...")

    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=-1)

    print("AI Model Loaded Successfully!")

# ----------------------------------------
# Load Saved Face Encodings
# ----------------------------------------

    known_faces = load_known_faces()
    
    print(f"{len(known_faces)} students loaded.")
    


# ----------------------------------------
# Open Camera
# ----------------------------------------

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        exit()

    print("Camera Started Successfully!")

# ----------------------------------------
# Main Loop
# ----------------------------------------

    while True:

        success, frame = camera.read()

        if not success:
            print("Could not read frame.")
            break

        # Detect faces
        faces = app.get(frame)

        for face in faces:

            # Face coordinates
            x1, y1, x2, y2 = face.bbox.astype(int)

            # Face embedding
            live_embedding = face.embedding

            # Recognize face
            name, similarity = recognize_face(
                live_embedding,
                known_faces
            )

            print(f"Recognized: {name} | Similarity: {similarity:.4f}")

            # ----------------------------
            # Default values
            # ----------------------------

            rectangle_color = (0, 0, 255)      # Red
            text_color = (0, 0, 255)

            display_name = "Unknown"
            status_message = "Unknown Person"

            # ----------------------------
            # Student Recognized
            # ----------------------------

            if name != "Unknown":

                student_name, roll_number = name.rsplit("_", 1)

                display_name = student_name

                rectangle_color = (0, 255, 0)

                student_id = get_student_id(
                    student_name,
                    roll_number
                )

                if student_id is not None:

                    

                    attendance_success, message = mark_attendance(student_id)

                    status_message = message

                    if attendance_success:
                        text_color = (0, 255, 0)
                    else:
                        text_color = (0, 255, 255)

                    print(message)
                else:

                    rectangle_color = (0, 0, 255)
                    text_color = (0, 0, 255)
                    status_message = "Student Not Found"

            # ----------------------------
            # Draw Rectangle
            # ----------------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                rectangle_color,
                2
            )

            # Student Name

            cv2.putText(
                frame,
                display_name,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                rectangle_color,
                2
            )

            # Status

            cv2.putText(
                frame,
                status_message,
                (x1, y2 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                text_color,
                2
            )

        cv2.imshow("AI Face Recognition Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# ----------------------------------------
# Cleanup
# ----------------------------------------
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_attendance()