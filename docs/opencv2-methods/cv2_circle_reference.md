# `cv2.circle()` Reference

## Overview

`cv2.circle()` draws a circle, outlined or filled, centered at a given point with a specified radius. It is applied to mark detected keypoints, centroids, or circular objects such as fiducial markers, and a filled circle is the standard way to highlight a single point location on an overlay. This is common in tracking and pose-estimation pipelines to visualize joint positions or target centers. The result is the image with a circle drawn at the given location, aiding visual verification of detection accuracy.

## Standard Syntax

```python
image = cv2.circle(image, center, radius, color[, thickness[, lineType[, shift]]])
```

Note: draws directly onto `image` **in place** and also returns it.

---

## Parameters in Detail

### `image` (input/output, required)
- Type: `numpy.ndarray`.
- The image to draw on. Modified in place.

### `center` (required)
- Type: tuple `(x, y)`.
- Center coordinates of the circle.

### `radius` (required)
- Type: `int`.
- Radius of the circle, in pixels.

### `color` (required)
- Type: tuple `(B, G, R)` for a color image, or `int` for grayscale.

### `thickness` (optional, default `1`)
- Type: `int`.
- Thickness of the circle outline, in pixels.
- Pass **`cv2.FILLED`** (or `-1`) to draw a solid filled circle instead of just an outline.

### `lineType` (optional, default `cv2.LINE_8`)
- Type of line used for the circle boundary:

| Constant | Behavior |
|---|---|
| `cv2.LINE_4` | 4-connected line |
| `cv2.LINE_8` | 8-connected line (default) |
| `cv2.LINE_AA` | Anti-aliased line (smoother circular edges) |

### `shift` (optional, default `0`)
- Type: `int`.
- Number of fractional bits in `center` coordinates and `radius` — allows sub-pixel precision. Rarely used in typical applications.

---

## Return Value

- Returns the same `image` array passed in (already modified in place).

---

## Basic Implementation Example

```python
import cv2

# 1. Load image
img = cv2.imread('frame.png')

# 2. Draw an outlined circle
cv2.circle(img, (200, 150), 50, (255, 0, 0), 2, cv2.LINE_AA)

# 3. Draw a filled circle marker at a detected point (e.g., a keypoint/centroid)
cv2.circle(img, (350, 300), 6, (0, 255, 0), cv2.FILLED)

# 4. Example: mark centroids of detected contours
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    M = cv2.moments(cnt)
    if M["m00"] == 0:
        continue
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

cv2.imshow('Circles', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Filled circles (`thickness=cv2.FILLED`) are the standard way to mark point detections — centroids, corner/keypoint detections, fiducial centers — on a debug overlay.
- Outlined circles are useful for highlighting a detected circular object (e.g., after `cv2.HoughCircles()`) without obscuring it.
- `cv2.LINE_AA` noticeably improves the visual smoothness of circle edges compared to the jagged default `LINE_8`, especially at small radii.
