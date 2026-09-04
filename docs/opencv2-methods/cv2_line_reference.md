# `cv2.line()` Reference

## Overview

`cv2.line()` draws a straight line segment between two points on an image, with configurable color, thickness, and anti-aliasing. It is applied to draw crosshairs at detected points, connect tracked keypoints or trajectories, or add reference/guide lines such as a horizon or boundary marker. In robotics vision overlays it is often used to visualize motion vectors or skeleton connections between joints. The outcome is the image with the line drawn directly onto it, useful for visual debugging and operator displays.

## Standard Syntax

```python
image = cv2.line(image, pt1, pt2, color[, thickness[, lineType[, shift]]])
```

Note: draws directly onto `image` **in place** and also returns it.

---

## Parameters in Detail

### `image` (input/output, required)
- Type: `numpy.ndarray`.
- The image to draw on. Modified in place.

### `pt1` (required)
- Type: tuple `(x, y)`.
- Starting point of the line segment.

### `pt2` (required)
- Type: tuple `(x, y)`.
- Ending point of the line segment.

### `color` (required)
- Type: tuple `(B, G, R)` for a color image, or `int` for grayscale.
- e.g. `(0, 0, 255)` for red.

### `thickness` (optional, default `1`)
- Type: `int`.
- Line thickness in pixels. Negative values (e.g. `cv2.FILLED`) are not meaningful for a line (unlike rectangles/circles) and are simply treated as the default.

### `lineType` (optional, default `cv2.LINE_8`)
- Type of line used:

| Constant | Behavior |
|---|---|
| `cv2.LINE_4` | 4-connected line |
| `cv2.LINE_8` | 8-connected line (default) |
| `cv2.LINE_AA` | Anti-aliased line (smoother, slightly slower) |

### `shift` (optional, default `0`)
- Type: `int`.
- Number of fractional bits in the point coordinates — allows sub-pixel precision by specifying coordinates scaled by `2**shift`. Rarely used in typical applications.

---

## Return Value

- Returns the same `image` array passed in (already modified in place).

---

## Basic Implementation Example

```python
import cv2

# 1. Load image
img = cv2.imread('frame.png')

# 2. Draw a simple diagonal line
cv2.line(img, (50, 50), (300, 300), (0, 0, 255), 2, cv2.LINE_AA)

# 3. Example: draw a crosshair at a detected point (e.g., object centroid)
cx, cy = 150, 150
size = 15
cv2.line(img, (cx - size, cy), (cx + size, cy), (0, 255, 0), 1)  # horizontal
cv2.line(img, (cx, cy - size), (cx, cy + size), (0, 255, 0), 1)  # vertical

cv2.imshow('Lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Commonly used to draw crosshairs/markers at detected centroids, connect keypoints (e.g., pose skeletons, tracked feature trails), or draw reference/guide lines (e.g., a horizon line, a conveyor boundary) on a live vision feed.
- `cv2.LINE_AA` is worth the small performance cost for any line meant for human viewing (debug overlays); default `LINE_8` is fine for lines used as part of a mask.
- For robotics telemetry overlays, lines are often drawn per-frame to show motion vectors or trajectory history — keep `thickness` small (1–2 px) to avoid cluttering the feed.
