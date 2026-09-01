# `cv2.rectangle()` Reference

## Standard Syntax

```python
image = cv2.rectangle(image, pt1, pt2, color[, thickness[, lineType[, shift]]])
```

Note: draws directly onto `image` **in place** and also returns it.

---

## Parameters in Detail

### `image` (input/output, required)
- Type: `numpy.ndarray`.
- The image to draw on. Modified in place.

### `pt1` (required)
- Type: tuple `(x, y)`.
- One corner of the rectangle — typically the **top-left**.

### `pt2` (required)
- Type: tuple `(x, y)`.
- The opposite corner of the rectangle — typically the **bottom-right**.

### `color` (required)
- Type: tuple `(B, G, R)` for a color image, or `int` for grayscale.

### `thickness` (optional, default `1`)
- Type: `int`.
- Thickness of the rectangle border, in pixels.
- Pass **`cv2.FILLED`** (or `-1`) to draw a solid filled rectangle instead of just an outline.

### `lineType` (optional, default `cv2.LINE_8`)
- Type of line used for the rectangle edges:

| Constant | Behavior |
|---|---|
| `cv2.LINE_4` | 4-connected line |
| `cv2.LINE_8` | 8-connected line (default) |
| `cv2.LINE_AA` | Anti-aliased line (rarely needed for straight axis-aligned edges, but supported) |

### `shift` (optional, default `0`)
- Type: `int`.
- Number of fractional bits in the point coordinates — allows sub-pixel precision. Rarely used in typical applications.

---

## Return Value

- Returns the same `image` array passed in (already modified in place).

---

## Basic Implementation Example

```python
import cv2

# 1. Load image
img = cv2.imread('frame.png')

# 2. Draw a simple outlined rectangle
cv2.rectangle(img, (50, 50), (200, 150), (0, 255, 0), 2)

# 3. Typical use: draw bounding boxes from findContours + boundingRect
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) < 500:
        continue
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(img, "Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 1, cv2.LINE_AA)

cv2.imshow('Rectangles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- This is the standard way to visualize `cv2.boundingRect()` results — draw the box, then usually `cv2.putText()` a label just above it.
- Use `thickness=cv2.FILLED` to create a solid rectangular mask or highlight a region (e.g., blacking out/redacting part of an image, or building a binary mask for further processing).
- `pt1`/`pt2` don't strictly need to be top-left/bottom-right — OpenCV normalizes any two opposite corners — but supplying them in that order keeps code readable and matches the `(x, y, w, h)` convention from `boundingRect`.
