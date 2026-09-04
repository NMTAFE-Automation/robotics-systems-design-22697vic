# `cv2.drawContours()` Reference

## Overview

`cv2.drawContours()` renders one or more contours (from `findContours()`) onto an image as outlines or filled shapes, either individually or all at once. It is used to visually verify detection results, build masks, or highlight regions of interest for a human viewer or a downstream masking step. Applied in a vision pipeline, it turns abstract point-list contours into a visible overlay on the original frame. The outcome is a modified image with the selected contour(s) drawn in the chosen color, thickness, and line style, ready for display or saving.

## Standard Syntax

```python
image = cv2.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]])
```

Note: the function draws directly onto `image` **in place** and also returns it (the return value is the same array object — useful for chaining, but not required).

---

## Parameters in Detail

### `image` (input/output, required)
- The image to draw on — typically a BGR color image (`numpy.ndarray`), so the contours show up in color.
- Modified in place.

### `contours` (required)
- The list of contours to draw, exactly as returned by `cv2.findContours()` — a Python `list` of `numpy.ndarray`s, each of shape `(n, 1, 2)`.

### `contourIdx` (required)
- Type: `int`.
- Index of the contour to draw from the `contours` list.
- Pass **`-1`** to draw **all** contours in the list.

### `color` (required)
- Type: tuple `(B, G, R)` for a color image, or a single `int` for grayscale.
- e.g. `(0, 255, 0)` for green.

### `thickness` (optional, default `1`)
- Type: `int`.
- Line thickness in pixels.
- Pass **`cv2.FILLED`** (or `-1`) to fill the interior of the contour(s) instead of just outlining.

### `lineType` (optional, default `cv2.LINE_8`)
- Type of line used:

| Constant | Behavior |
|---|---|
| `cv2.LINE_4` | 4-connected line |
| `cv2.LINE_8` | 8-connected line (default) |
| `cv2.LINE_AA` | Anti-aliased line (smoother edges, slightly slower) |

### `hierarchy` (optional, default `None`)
- The hierarchy array returned by `cv2.findContours()`.
- Required only if you want to limit drawing by `maxLevel`.

### `maxLevel` (optional, default very large / draws all)
- Type: `int`.
- Controls how deep into the contour hierarchy to draw when `hierarchy` is supplied:
  - `0`: draw only the specified contour.
  - `1`: draw the contour and its immediate nested contours (children).
  - `2+`: draw further nested levels, and so on.

### `offset` (optional, default `(0, 0)`)
- Type: tuple `(x, y)`.
- Shifts all contour points before drawing — useful if the contours were computed on a cropped/offset region but you're drawing onto the full original image.

---

## Basic Implementation Example

```python
import cv2

# 1. Load image, convert to grayscale, threshold
img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 2. Find contours
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 3. Draw ALL contours in green, outline only
output = img.copy()
cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

# 4. Draw just the largest contour, filled, in red on a separate copy
largest = max(contours, key=cv2.contourArea)
filled = img.copy()
cv2.drawContours(filled, [largest], -1, (0, 0, 255), cv2.FILLED)

cv2.imshow('All Contours', output)
cv2.imshow('Largest Filled', filled)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- To draw a single contour, wrap it in a list: `cv2.drawContours(img, [contours[i]], -1, color, thickness)` — passing `contours[i]` directly (without brackets) is a common mistake that raises an error, since the function expects a list of contours.
- Use `thickness=cv2.FILLED` to create solid masks from contours (handy for masking out detected regions in a robotics/vision pipeline).
- `cv2.LINE_AA` looks best for visual output/debug overlays; stick with `cv2.LINE_8` (default) for masks used in further processing to avoid partial-intensity edge pixels.
