# `cv2.adaptiveThreshold()` Reference

## Standard Syntax

```python
dst = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C[, dst])
```

---

## Parameters in Detail

### `src` (input, required)
- Type: `numpy.ndarray`.
- Input image — must be single-channel 8-bit grayscale.

### `maxValue` (required)
- Type: `float`.
- Value assigned to pixels that satisfy the threshold condition (analogous to `maxval` in `cv2.threshold()`).

### `adaptiveMethod` (required)
- Type: adaptive method constant. Determines how the local threshold is computed for each pixel neighborhood:

| Constant | Behavior |
|---|---|
| `cv2.ADAPTIVE_THRESH_MEAN_C` | Threshold = mean of the neighborhood area, minus constant `C`. |
| `cv2.ADAPTIVE_THRESH_GAUSSIAN_C` | Threshold = Gaussian-weighted sum of the neighborhood, minus constant `C` (generally smoother/better results than mean). |

### `thresholdType` (required)
- Type: threshold type constant. Only two are valid here:

| Constant | Behavior |
|---|---|
| `cv2.THRESH_BINARY` | `dst = maxValue` if `src(x,y) > local_thresh`, else `0`. |
| `cv2.THRESH_BINARY_INV` | Inverse of the above. |

### `blockSize` (required)
- Type: `int`, must be **odd** and greater than `1` (e.g., `3`, `11`, `21`).
- Size of the pixel neighborhood used to calculate the local threshold for each pixel.
- Larger block size = threshold adapts more slowly/smoothly across the image; smaller = more locally sensitive (but noisier).

### `C` (required)
- Type: `float` (can be negative).
- A constant subtracted from the computed mean/weighted-mean for each neighborhood — fine-tunes sensitivity. Higher `C` → stricter (fewer pixels pass); lower/negative `C` → more lenient.

### `dst` (optional)
- Output array; usually omitted and taken from the return value instead.

---

## Return Value

- `dst`: a `numpy.ndarray`, same size as `src`, containing the binary image where each pixel was thresholded against its own local neighborhood value.

---

## Basic Implementation Example

```python
import cv2

# 1. Load image and convert to grayscale
img = cv2.imread('unevenly_lit_document.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Reduce noise slightly before adaptive thresholding
blurred = cv2.medianBlur(gray, 5)

# 3. Apply adaptive thresholding (Gaussian-weighted, local neighborhoods)
adaptive = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    blockSize=11,
    C=2
)

cv2.imshow('Original Gray', gray)
cv2.imshow('Adaptive Threshold', adaptive)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Use this instead of `cv2.threshold()` when lighting is **uneven across the frame** — e.g., a Raspberry Pi camera viewing a scene with shadows, glare, or a gradient of ambient light. A single global threshold would fail in the darker/brighter regions; adaptive thresholding computes a different threshold per local neighborhood.
- `ADAPTIVE_THRESH_GAUSSIAN_C` generally produces smoother, less noisy results than `ADAPTIVE_THRESH_MEAN_C` and is the more common choice in practice.
- `blockSize` and `C` typically need hand-tuning per application — start with `blockSize=11, C=2` as a reasonable default and adjust based on results.
- A light blur (`cv2.medianBlur` or `cv2.GaussianBlur`) before adaptive thresholding helps suppress sensor noise that would otherwise create speckled artifacts in the output.
