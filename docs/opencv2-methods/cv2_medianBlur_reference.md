# `cv2.medianBlur()` Reference

## Overview

`cv2.medianBlur()` replaces each pixel with the median value of its surrounding neighborhood, which is highly effective at removing salt-and-pepper (impulse) noise while preserving sharp edges. It is applied when a camera or sensor produces random pixel dropouts, common on cheaper hardware or in electrically noisy environments. Compared to Gaussian blur it does a better job protecting edges, making it a good pre-step before thresholding or adaptive thresholding. The outcome is a cleaned image with isolated noisy pixels removed and object boundaries left largely intact.

## Standard Syntax

```python
dst = cv2.medianBlur(src, ksize[, dst])
```

---

## Parameters in Detail

### `src` (input, required)
- Type: `numpy.ndarray`.
- Input image with 1, 3, or 4 channels.
- For `ksize` greater than `5`, image depth must be `CV_8U` (standard 8-bit images); for `ksize` of `3` or `5`, `CV_8U`, `CV_16U`, or `CV_32F` are supported.

### `ksize` (required)
- Type: `int` (a single odd integer, **not** a tuple like in `GaussianBlur`).
- Aperture linear size — must be odd and greater than `1` (e.g., `3`, `5`, `7`).
- Each output pixel is the **median** of the `ksize x ksize` neighborhood around the corresponding input pixel.

### `dst` (optional)
- Output array; usually omitted and taken from the return value instead.

---

## Return Value

- `dst`: a `numpy.ndarray`, same size and type as `src`, containing the median-filtered image.

---

## Basic Implementation Example

```python
import cv2

# 1. Load an image with salt-and-pepper style noise
img = cv2.imread('salt_pepper_noise.png')

# 2. Apply median blur to remove impulse noise while preserving edges
denoised = cv2.medianBlur(img, 5)

# 3. Compare with Gaussian blur on the same image
gaussian = cv2.GaussianBlur(img, (5, 5), 0)

cv2.imshow('Original', img)
cv2.imshow('Median Blur', denoised)
cv2.imshow('Gaussian Blur', gaussian)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- `cv2.medianBlur()` is the go-to filter for **salt-and-pepper noise** (random black/white pixel dropouts) — common with cheap camera sensors or noisy digital I/O captures — because it removes outlier pixel values while preserving edges much better than Gaussian blur.
- Unlike Gaussian blur, it does not blur edges as heavily, making it a good preprocessing step before contour/edge-based detection when the noise is impulsive rather than smooth.
- Computationally more expensive than Gaussian blur for large kernel sizes, which can matter on resource-constrained hardware like a Raspberry Pi running a real-time vision loop.
