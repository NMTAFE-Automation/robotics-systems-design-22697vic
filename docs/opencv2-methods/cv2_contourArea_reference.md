# `cv2.contourArea()` Reference

## Overview

`cv2.contourArea()` calculates the enclosed area of a contour from its vertex coordinates (via Green's theorem), giving a single numeric size measurement for a detected shape. It is most often applied as a filtering step right after `findContours()`, to separate real objects from tiny noise contours caused by sensor grain or lighting artifacts. It is also used to rank contours by size (e.g., picking the largest blob) or to compute shape descriptors like circularity. The outcome is a floating-point area value per contour that drives decisions elsewhere in the pipeline — keep or discard, sort, or compare.

## Standard Syntax

```python
area = cv2.contourArea(contour[, oriented])
```

---

## Parameters in Detail

### `contour` (input, required)
- Type: `numpy.ndarray` of shape `(n, 1, 2)` — a single contour, as returned in the `contours` list from `cv2.findContours()`.
- Must be a single contour, not the whole list (pass `contours[i]`, not `contours`).

### `oriented` (optional, default `False`)
- Type: `bool`.
- If `False` (default): returns the **absolute** area as a positive `float`.
- If `True`: returns a **signed** area, whose sign indicates the contour's orientation (clockwise vs. counter-clockwise). This is mainly used to determine orientation programmatically, e.g. to check whether contours are nested consistently.

---

## Return Value

- A `float` representing the area enclosed by the contour, computed using Green's theorem (based on the contour's vertices — **not** a pixel count of the filled region, so it can differ slightly from `cv2.countNonZero()` on a filled mask).

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

# 3. Compute area of each contour and filter out noise
min_area = 500  # tune based on expected object size
output = img.copy()

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < min_area:
        continue  # skip small/noisy contours
    cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)
    print(f"Contour area: {area:.1f}")

cv2.imshow('Filtered Contours', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- The single most common use is **noise filtering**: after thresholding/edge detection, small spurious contours often appear from sensor noise or lighting artifacts — discard any contour below a minimum area threshold before further processing.
- Because it's a polygon-based (Green's theorem) calculation rather than a raw pixel count, very small or degenerate contours (e.g., fewer than 3 points, or collinear points) can report `0.0`.
- Often combined with `cv2.arcLength()` (perimeter) and `cv2.boundingRect()` (bounding box) to build shape descriptors — e.g., circularity = `4 * π * area / (perimeter ** 2)`, useful for identifying circular fiducials or markers.
