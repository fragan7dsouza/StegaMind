import os
import pickle
from PIL import Image
import numpy as np

src = r"C:\Users\FraganDsouza\Desktop\cifar-10-batches-py"
dst = "data/secrets"

os.makedirs(dst, exist_ok=True)

def load_batch(path):
    with open(path, "rb") as f:
        d = pickle.load(f, encoding="bytes")
    return d[b"data"]

batches = [
    "data_batch_1",
    "data_batch_2",
    "data_batch_3",
    "data_batch_4",
    "data_batch_5"
]

i = 0
for b in batches:
    p = os.path.join(src, b)
    if not os.path.exists(p):
        continue
    data = load_batch(p)
    for img in data:
        img = img.reshape(3, 32, 32).transpose(1, 2, 0)
        img = Image.fromarray(img).resize((128, 128))
        img.save(os.path.join(dst, f"cifar_{i}.jpg"))
        i += 1

print("done:", i, "images")
