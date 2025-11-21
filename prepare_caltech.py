import os
import glob
from PIL import Image

src = r"C:\Users\FraganDsouza\Desktop\caltech-101\101_ObjectCategories"
dst = "data/cover_images"

os.makedirs(dst, exist_ok=True)
classes = glob.glob(os.path.join(src, "*"))

i = 0
for c in classes:
    imgs = glob.glob(os.path.join(c, "*.jpg"))
    for path in imgs:
        try:
            img = Image.open(path).convert("RGB").resize((128, 128))
            img.save(os.path.join(dst, f"caltech_{i}.jpg"))
            i += 1
        except:
            pass

print("done:", i, "images")
