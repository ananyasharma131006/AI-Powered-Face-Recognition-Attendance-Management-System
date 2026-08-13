from insightface.app import FaceAnalysis
import cv2
import numpy as np

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    faces = app.get(frame)

    if len(faces) > 0:
        emb = faces[0].embedding

        print("Shape:", emb.shape)
        print("Type:", emb.dtype)
        print("Norm:", np.linalg.norm(emb))

        break

camera.release()