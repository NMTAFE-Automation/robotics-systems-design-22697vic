# `cv2.GaussianBlur()` Reference

## Standard Syntax

```python
dst = cv2.GaussianBlur(src, ksize, sigmaX[, dst[, sigmaY[, borderType]]])
```

---

## Parameters in Detail

### `src` (input, required)
- Type: `numpy.ndarray`.
- Input image, any number of channels, processed independently per channel.

### `ksize` (required)
- Type: tuple `(width, height)`.
- Gaussian kernel size. **Both values must be positive and odd** (e.g., `(3, 3)`, `(5, 5)`, `(9, 9)`).
- Pass `(0, 0)` to have the kernel size computed automatically from `sigmaX`.
- Larger kernel = stronger blur.

### `sigmaX` (required)
- Type: `float`.
- Gaussian kernel standard deviation in the X direction.
- If set to `0`, it is computed automatically from `ksize`.

### `dst` (optional)
- Output array; usually omitted and taken from the return value instead.

### `sigmaY` (optional, default `0`)
- Type: `float`.
- Gaussian kernel standard deviation in the Y direction.
- If `0`, it is set equal to `sigmaX`. If both `sigmaX` and `sigmaY` are `0`, they're derived from `ksize`.

### `borderType` (optional, default `cv2.BORDER_DEFAULT`)
- Type: border extrapolation method constant (e.g. `cv2.BORDER_CONSTANT`, `cv2.BORDER_REPLICATE`, `cv2.BORDER_REFLECT`).
- Controls how pixels at the image edges are extrapolated during convolution.

---

## Return Value

- `dst`: a `numpy.ndarray`, same size and type as `src`, containing the blurred image.

---

## Basic Implementation Example

```python
import cv2

# 1. Load image
img = cv2.imread('noisy_image.png')

# 2. Apply Gaussian blur to reduce noise before edge detection
blurred = cv2.GaussianBlur(img, (5, 5), sigmaX=0)

# 3. Typical pipeline: blur -> grayscale -> edge detection
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

cv2.imshow('Original', img)
cv2.imshow('Blurred', blurred)
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Gaussian blur is the standard noise-reduction step **before** `cv2.Canny()` edge detection or thresholding — raw sensor noise otherwise produces many spurious edges/contours.
- Larger `ksize` removes more noise but also smooths away fine detail and small objects — tune based on expected object/feature size in the frame.
- Unlike `cv2.medianBlur()`, Gaussian blur is a weighted average, so it's not as effective against salt-and-pepper (impulse) noise but is faster and gives smoother results for general Gaussian-distributed sensor noise.
