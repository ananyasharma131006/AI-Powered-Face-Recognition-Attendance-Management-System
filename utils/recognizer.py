from pathlib import Path
import numpy as np

# Cosine similarity threshold
THRESHOLD = 0.45


def load_known_faces():
    """
    Load all saved face embeddings.
    """
    known_faces = {}

    encoding_folder = Path("encodings")

    if not encoding_folder.exists():
        return known_faces

    for file in encoding_folder.glob("*.npy"):
        name = file.stem
        embedding = np.load(file)
        known_faces[name] = embedding

    return known_faces


def recognize_face(live_embedding, known_faces):
    """
    Compare the live embedding with all saved embeddings
    using Cosine Similarity.
    """

    best_match = "Unknown"
    highest_similarity = -1.0

    # Normalize live embedding
    live_embedding = live_embedding / np.linalg.norm(live_embedding)

    for name, saved_embedding in known_faces.items():

        # Normalize saved embedding
        saved_embedding = saved_embedding / np.linalg.norm(saved_embedding)

        # Cosine similarity
        similarity = np.dot(live_embedding, saved_embedding)

        print(f"{name} : Similarity = {similarity:.4f}")

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = name

    if highest_similarity >= THRESHOLD:
        return best_match, highest_similarity

    return "Unknown", highest_similarity


if __name__ == "__main__":

    faces = load_known_faces()

    print("\nLoaded Students:\n")

    for student in faces:
        print(student)