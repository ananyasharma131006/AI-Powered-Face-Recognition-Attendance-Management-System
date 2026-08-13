from insightface.app import FaceAnalysis

print("Loading model...")

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

print("Success!")