from insightface.app import FaceAnalysis

print("Loading Face Detector...")

# Load InsightFace model
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

print("Face Detector Ready!")


def detect_faces(frame):
    """
    Detect faces using InsightFace.
    Returns a list of (x, y, w, h).
    """

    faces = app.get(frame)

    boxes = []

    for face in faces:

        x1, y1, x2, y2 = face.bbox.astype(int)

        boxes.append((x1, y1, x2 - x1, y2 - y1))

    return boxes