# `cv2.inRange()` Reference

## Overview

`cv2.inRange()` checks every pixel of an image against a lower and an upper bound and creates a binary mask. Pixels inside the range become white (255) and pixels outside become black (0). It is mostly used with the HSV color space to detect objects by color, for example a red ball, a green marker or a yellow line. The result is a single-channel mask that you can clean with morphology, pass to `cv2.findContours()`, or use with `cv2.bitwise_and()` to cut out the colored object.

## Standard Syntax

```python
dst = cv2.inRange(src, lowerb, upperb[, dst])
```

---

## Parameters in Detail

### `src` (input, required)
- Type: `numpy.ndarray`.
- Input image. It can be single-channel (grayscale) or multi-channel (BGR, HSV).
- For color detection, convert the image to HSV first with `cv2.cvtColor(img, cv2.COLOR_BGR2HSV)`.

### `lowerb` (required)
- Type: tuple, list, `numpy.ndarray` or scalar.
- Lower boundary (inclusive). For a 3-channel image, give 3 values, for example `(H_min, S_min, V_min)`.

### `upperb` (required)
- Type: tuple, list, `numpy.ndarray` or scalar.
- Upper boundary (inclusive). Same size as `lowerb`, for example `(H_max, S_max, V_max)`.
- A pixel is white only if **every channel** is between the lower and upper value.

### `dst` (optional)
- Output array. Usually left out and taken from the return value.

### HSV value ranges in OpenCV

| Channel | Meaning | OpenCV range |
|---|---|---|
| H (Hue) | Color type (red, green, blue...) | 0 to 179 (not 0 to 360) |
| S (Saturation) | Color strength (0 = gray/white) | 0 to 255 |
| V (Value) | Brightness (0 = black) | 0 to 255 |

### Common hue values (approximate)

| Color | Hue range |
|---|---|
| Red | 0 to 10 and 170 to 179 (red wraps around, needs two masks) |
| Orange | 10 to 25 |
| Yellow | 25 to 35 |
| Green | 35 to 85 |
| Blue | 90 to 130 |
| Purple / Magenta | 130 to 169 |

---

## Return Value

- `dst`: a single-channel `uint8` `numpy.ndarray` with the same height and width as `src`. Values are only `255` (inside range) or `0` (outside range).

---

## Basic Implementation Example

```python
import cv2
import numpy as np

# 1. Load image (OpenCV loads as BGR)
img = cv2.imread('objects.png')

# 2. Reduce noise, then convert to HSV
blurred = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

# 3. Define the range for GREEN (tune these for your camera and lighting)
lower_green = np.array([35, 80, 60])
upper_green = np.array([85, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)

# 4. Clean the mask (remove small specks, fill small holes)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# 5. Find the contours of the detected color regions
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

output = img.copy()
for cnt in contours:
    if cv2.contourArea(cnt) < 500:
        continue  # ignore small noise
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(output, "Green", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

# 6. Keep only the green pixels from the original image
green_only = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('Mask', mask)
cv2.imshow('Detected', output)
cv2.imshow('Green Only', green_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Example: detecting RED (two ranges)

Red is at both ends of the hue scale, so you need two masks and combine them:

```python
lower_red1 = np.array([0, 120, 70]);    upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70]);  upper_red2 = np.array([179, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)
```

---

## Practical Notes

HSV is better than BGR for color detection because Hue stays almost the same when the light gets brighter or darker, so the same range works in more lighting conditions. On a Raspberry Pi camera, lighting still changes the Saturation and Value, so set the lower S and V limits high enough to ignore gray and dark areas (for example S above 80 and V above 60). The best way to find good values is to print the HSV of a sample pixel, or to use `cv2.createTrackbar()` with six sliders and tune the range live. Always use a light blur before `cv2.cvtColor()` and clean the mask with `cv2.morphologyEx()` before `cv2.findContours()`, otherwise noise creates many false contours. Remember that in OpenCV the hue goes only from 0 to 179, so values copied from a normal color picker (0 to 360) must be divided by 2.
