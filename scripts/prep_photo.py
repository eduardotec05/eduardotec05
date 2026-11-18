#!/usr/bin/env python3
"""
Prepare the profile photo for clean ASCII conversion:
  1. Remove / isolate background so the subject is crisp
  2. Bilateral filter smoothing to reduce photographic grain
  3. CLAHE contrast-limited adaptive histogram equalization
  4. Difference-of-Gaussians edge accentuation
  5. Composite onto pure white background (maps to spaces in ASCII ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

LINE_WEIGHT = 0.55

img = cv2.imread(INP)
if img is None:
    print(f"Error: could not read {INP}", file=sys.stderr)
    sys.exit(1)

h, w = img.shape[:2]

# 1. GrabCut foreground isolation with margin
mask = np.zeros((h, w), np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (int(w * 0.06), int(h * 0.04), int(w * 0.88), int(h * 0.94))
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 6, cv2.GC_INIT_WITH_RECT)
fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype("uint8")

# Smooth edges of mask
fg_mask = cv2.GaussianBlur(fg_mask, (7, 7), 0)

# 2. Convert to grayscale & smooth texture while keeping edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
smooth = gray
for _ in range(3):
    smooth = cv2.bilateralFilter(smooth, 9, 45, 9)

# 3. CLAHE (Local Adaptive Contrast)
clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
contrast = clahe.apply(smooth)

# 4. Difference-of-Gaussians for sharp features (eyes, nose, outline)
fine = cv2.GaussianBlur(contrast, (0, 0), 1.2).astype(np.float32)
coarse = cv2.GaussianBlur(contrast, (0, 0), 5.0).astype(np.float32)
lines = np.clip((coarse - fine) / 36.0, 0, 1)

# Tone stretch over the subject area
subj_pixels = contrast[fg_mask > 80]
if len(subj_pixels) > 0:
    lo, hi = np.percentile(subj_pixels, [3, 94])
    tone = np.clip((contrast.astype(np.float32) - lo) / (hi - lo), 0, 1)
else:
    tone = contrast.astype(np.float32) / 255.0

enhanced = np.clip(tone - LINE_WEIGHT * lines, 0, 1) * 255.0

# 5. Composite onto pure white where background is
alpha = (fg_mask.astype(np.float32) / 255.0) ** 1.3
final = (enhanced * alpha + 255.0 * (1.0 - alpha)).astype(np.uint8)

cv2.imwrite(OUT, final)
print(f"wrote {OUT} ({w}x{h})")
