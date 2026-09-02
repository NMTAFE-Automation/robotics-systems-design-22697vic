# `cv2.threshold()` Reference

## Standard Syntax

```python
retval, dst = cv2.threshold(src, thresh, maxval, type[, dst])
```

---

## Parameters in Detail

### `src` (input, required)
- Type: `numpy.ndarray`.
- Input image — typically single-channel (grayscale), though multi-channel is allowed for some threshold types.

### `thresh` (required)
- Type: `float`.
- The threshold value used to classify pixel values.

### `maxval` (required)
- Type: `float`.
- The value assigned to pixels that pass the threshold condition, used with `cv2.THRESH_BINARY` and `cv2.THRESH_BINARY_INV`.

### `type` (required)
- Type: thresholding type constant. Determines how pixels are classified:

| Constant | Behavior |
|---|---|
| `cv2.THRESH_BINARY` | `dst = maxval` if `src > thresh`, else `0`. |
| `cv2.THRESH_BINARY_INV` | `dst = 0` if `src > thresh`, else `maxval` (inverse of above). |
| `cv2.THRESH_TRUNC` | `dst = thresh` if `src > thresh`, else `src` unchanged (caps values). |
| `cv2.THRESH_TOZERO` | `dst = src` if `src > thresh`, else `0`. |
| `cv2.THRESH_TOZERO_INV` | `dst = 0` if `src > thresh`, else `src` unchanged. |
| `cv2.THRESH_OTSU` | Combine with a flag (e.g. `cv2.THRESH_BINARY + cv2.THRESH_OTSU`) to auto-compute the optimal threshold using Otsu's method — `thresh` argument is then ignored (pass `0`). |
| `cv2.THRESH_TRIANGLE` | Combine similarly to auto-compute threshold using the triangle algorithm — good for images with a single dominant peak in the histogram. |

### `dst` (optional)
- Output array; usually omitted and taken from the return value instead.

---

## Return Values

Returns a tuple `(retval, dst)`:

| Value | Meaning |
|---|---|
| `retval` | The threshold value actually used. Equal to `thresh` for standard modes, or the **computed** optimal threshold when using `THRESH_OTSU`/`THRESH_TRIANGLE`. |
| `dst` | The thresholded (binary or modified) output image, same size as `src`. |

---

## Basic Implementation Example

```python
import cv2

# 1. Load image and convert to grayscale
img = cv2.imread('document.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Simple fixed-threshold binarization
retval, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print(f"Threshold used: {retval}")

# 3. Otsu's method — automatically determines the optimal threshold
retval_otsu, binary_otsu = cv2.threshold(
    gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)
print(f"Otsu-computed threshold: {retval_otsu}")

cv2.imshow('Fixed Threshold', binary)
cv2.imshow('Otsu Threshold', binary_otsu)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- Use a fixed `thresh` value when lighting is controlled/consistent (e.g., a fixed industrial camera setup).
- Use `cv2.THRESH_OTSU` when lighting varies between runs but is still roughly uniform across the frame — it picks the threshold automatically from the image's histogram, removing manual tuning.
- If lighting is **uneven across the frame** (shadows, spotlights, uneven ambient light — common with a Pi camera in a real environment), global thresholding (including Otsu) will fail in parts of the image; use `cv2.adaptiveThreshold()` instead.
- Always combine with `cv2.THRESH_BINARY` (or another mode) via `+` when using `THRESH_OTSU`/`THRESH_TRIANGLE` — they are modifier flags, not standalone modes.

### Links

- https://www.geeksforgeeks.org/python/simple-thresholdin-using-opencv/