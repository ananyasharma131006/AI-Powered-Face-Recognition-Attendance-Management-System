import numpy as np

e = np.load("encodings/Ananya_1.npy")

print("Shape:", e.shape)
print("Type:", e.dtype)
print("Norm:", np.linalg.norm(e))