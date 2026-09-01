# `cv2.boundingRect()` Reference

## Standard Syntax

```python
x, y, w, h = cv2.boundingRect(array)
```

---

## Parameters in Detail

### `array` (input, required)
- Type: either
  - a single contour — a `numpy.ndarray` of shape `(n, 1, 2)`, as returned in the `contours` list from `cv2.findContours()`, **or**
  - a grayscale/binary image where non-zero pixels define the shape.
- Represents the 2D point set (or object) for which the up-right bounding box is computed.

*(This function takes no other parameters — it's one of the simpler OpenCV geometry functions.)*

---

## Return Values

Returns a 4-tuple `(x, y, w, h)`:

| Value | Meaning |
|---|---|
| `x` | x-coordinate of the top-left corner of the bounding rectangle |
| `y` | y-coordinate of the top-left corner of the bounding rectangle |
| `w` | width of the bounding rectangle |
| `h` | height of the bounding rectangle |

The rectangle is always **axis-aligned** (not rotated) — for a minimum-area *rotated* rectangle, use `cv2.minAreaRect()` instead.

---

## Basic Implementation Example

```python
import cv2

# 1. Load image, convert to grayscale, threshold
img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 2. Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3. Get bounding box for each contour and draw it
output = img.copy()
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(output, (x, y), (x + w, y + h), (255, 0, 0), 2)
    print(f"Bounding box: x={x}, y={y}, w={w}, h={h}")

cv2.imshow('Bounding Boxes', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Commonly paired with `cv2.contourArea()` to filter small/noisy contours before computing bounding boxes.
- Useful in robotics/vision pipelines for cropping a region of interest (ROI) around a detected object: `roi = img[y:y+h, x:x+w]`.
- Aspect ratio (`w / h`) from the bounding box is a cheap way to distinguish shapes (e.g., filtering for roughly-square fiducial markers before further processing).
- For objects that are rotated relative to the camera, an axis-aligned box may be much larger than the object itself — consider `cv2.minAreaRect()` for a tighter fit in that case.
