# `cv2.findContours()` Reference

## Standard Syntax

**OpenCV 4.x (current):**
```python
contours, hierarchy = cv2.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
```

**OpenCV 3.x (older, for reference):**
```python
image, contours, hierarchy = cv2.findContours(image, mode, method)
```
(v3 returned three values; v4 dropped the modified-image return.)

---

## Parameters in Detail

### `image` (input, required)
- Type: single-channel 8-bit image (binary), e.g. `numpy.ndarray` of dtype `uint8`.
- Non-zero pixels are treated as 1, zero pixels as 0 — so you almost always feed it the output of `cv2.threshold()` or `cv2.Canny()` first.
- Since OpenCV 3.2+, the source image is **not modified** in place (earlier versions overwrote it).

### `mode` (retrieval mode, required)
Controls which contours are returned and how hierarchy is built:

| Constant | Behavior |
|---|---|
| `cv2.RETR_EXTERNAL` | Retrieves only the extreme outer contours. Ignores holes/nested contours. |
| `cv2.RETR_LIST` | Retrieves all contours without establishing any parent-child hierarchy. |
| `cv2.RETR_CCOMP` | Retrieves all contours, organizes into a 2-level hierarchy (outer boundaries and holes). |
| `cv2.RETR_TREE` | Retrieves all contours and reconstructs a full nested hierarchy tree. |
| `cv2.RETR_FLOODFILL` | Uses flood-fill style retrieval (works with signed 32-bit input image). |

### `method` (contour approximation method, required)
Controls how many points are stored per contour:

| Constant | Behavior |
|---|---|
| `cv2.CHAIN_APPROX_NONE` | Stores *all* boundary points (no compression). |
| `cv2.CHAIN_APPROX_SIMPLE` | Compresses horizontal, vertical, and diagonal segments, keeping only their endpoints (e.g., a rectangle → 4 points). Most commonly used — saves memory. |
| `cv2.CHAIN_APPROX_TC89_L1` | Applies the Teh-Chin chain approximation algorithm (variant 1). |
| `cv2.CHAIN_APPROX_TC89_KCOS` | Applies the Teh-Chin chain approximation algorithm (variant 2, k-cosine). |

### `offset` (optional)
- Type: tuple `(x, y)`, default `(0, 0)`.
- Shifts every contour point by this offset. Useful when contours were found in a cropped ROI but need to be mapped back onto the coordinates of the original full image.

### Return Values
- **`contours`**: a Python `list` where each element is a `numpy.ndarray` of shape `(n, 1, 2)` — the `(x, y)` coordinates of the `n` points making up one contour.
- **`hierarchy`**: a `numpy.ndarray` of shape `(1, n, 4)`. For each contour `i`, `hierarchy[0][i] = [next, previous, first_child, parent]` — indices into the contours list, or `-1` if none exists.

---

## Basic Implementation Example

```python
import cv2
import numpy as np

# 1. Load image and convert to grayscale
img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Threshold to get a binary image (contours need a binary input)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 3. Find contours
contours, hierarchy = cv2.findContours(
    binary,
    cv2.RETR_TREE,          # retrieve full hierarchy
    cv2.CHAIN_APPROX_SIMPLE # compress redundant points
)

print(f"Number of contours found: {len(contours)}")

# 4. Draw contours on a copy of the original image
output = img.copy()
cv2.drawContours(output, contours, -1, (0, 255, 0), 2)  # -1 = draw all contours

# 5. Example: get bounding box + area of each contour
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    print(f"Contour {i}: area={area:.1f}, bbox=({x},{y},{w},{h})")

cv2.imshow('Contours', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

For robotics/vision pipelines (e.g., fiducial or blob detection on a Pi camera feed):

- Use `RETR_EXTERNAL` + `CHAIN_APPROX_SIMPLE` when you only care about outer object silhouettes (fastest, least noise).
- Filter tiny contours by `cv2.contourArea()` before acting on them to reject sensor noise.
