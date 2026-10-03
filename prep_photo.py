"""Prep a photo for ASCII conversion: remove bg, boost local contrast, put on white."""
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove

src = sys.argv[1]
rgba = remove(Image.open(src).convert("RGB")).convert("RGBA")
bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
bg.alpha_composite(rgba)
gray = cv2.cvtColor(np.array(bg.convert("RGB")), cv2.COLOR_RGB2GRAY)
mask = np.array(rgba)[:, :, 3] > 10
eq = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
eq[~mask] = 255
cv2.imwrite("source-prepped.png", eq)
print("wrote source-prepped.png")
