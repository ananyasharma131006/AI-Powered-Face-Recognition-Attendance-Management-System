from pathlib import Path
import cv2
import numpy as np
from insightface.app import FaceAnalysis

print("Loading AI model...")

# Load InsightFace model
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

print("AI Model Loaded Successfully!")


def generate_embedding(image_path):
    """
    Generates a face embedding from an image.
    Returns None if no face is detected.
    """

    image = cv2.imread(str(image_path))

    if image is None:
        return None

    faces = app.get(image)

    if len(faces) == 0:
        return None

    # Use the first detected face
    return faces[0].embedding


def encode_student(student_folder):
    """
    Generates one average embedding for a student.
    """

    embeddings = []

    images = sorted(student_folder.glob("*.jpg"))

    print(f"\nProcessing {len(images)} images...")

    for image in images:

        embedding = generate_embedding(image)

        if embedding is not None:
            embeddings.append(embedding)
            print(f"✓ {image.name}")
        else:
            print(f"✗ No face detected: {image.name}")

    if len(embeddings) == 0:
        print("No valid faces found.")
        return

    average_embedding = np.mean(embeddings, axis=0)

    Path("encodings").mkdir(exist_ok=True)

    save_path = Path("encodings") / f"{student_folder.name}.npy"

    np.save(save_path, average_embedding)

    print("\n=================================")
    print("Student Encoding Saved Successfully!")
    print(f"Saved to: {save_path}")
    print("=================================")


def generate_student_encoding(student_name, roll_number):
    """
    Generates and saves the face encoding for a registered student.
    """

    folder = Path("images") / f"{student_name}_{roll_number}"

    if folder.exists():
        encode_student(folder)
        return True

    return False


if __name__ == "__main__":

    student_name = input("Enter Student Name: ")
    roll_number = input("Enter Roll Number: ")

    generate_student_encoding(student_name, roll_number)