# `cv2.putText()` Reference

## Standard Syntax

```python
image = cv2.putText(image, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
```

Note: like `drawContours`, this draws directly onto `image` **in place** and also returns it.

---

## Parameters in Detail

### `image` (input/output, required)
- Type: `numpy.ndarray`.
- The image to draw text on. Modified in place.

### `text` (required)
- Type: `str`.
- The text string to render.

### `org` (required)
- Type: tuple `(x, y)`.
- Coordinates of the **bottom-left corner** of the text string (by default — see `bottomLeftOrigin`).

### `fontFace` (required)
- Type: font constant. Selects the typeface:

| Constant | Style |
|---|---|
| `cv2.FONT_HERSHEY_SIMPLEX` | Normal sans-serif (most commonly used) |
| `cv2.FONT_HERSHEY_PLAIN` | Small sans-serif |
| `cv2.FONT_HERSHEY_DUPLEX` | Sans-serif, more complex/refined than simplex |
| `cv2.FONT_HERSHEY_COMPLEX` | Serif-style, normal size |
| `cv2.FONT_HERSHEY_TRIPLEX` | Serif-style, more complex than complex |
| `cv2.FONT_HERSHEY_COMPLEX_SMALL` | Smaller version of complex |
| `cv2.FONT_HERSHEY_SCRIPT_SIMPLEX` | Hand-writing style |
| `cv2.FONT_HERSHEY_SCRIPT_COMPLEX` | More complex hand-writing style |
| `cv2.FONT_ITALIC` | Flag that can be OR'd with any of the above to italicize |

### `fontScale` (required)
- Type: `float`.
- Scale factor multiplied by the font's base size — controls text size (e.g., `0.5`, `1`, `2`).

### `color` (required)
- Type: tuple `(B, G, R)` for a color image, or `int` for grayscale.
- e.g. `(0, 255, 0)` for green text.

### `thickness` (optional, default `1`)
- Type: `int`.
- Line thickness of the text strokes, in pixels. Larger = bolder text.

### `lineType` (optional, default `cv2.LINE_8`)
- Type of line used to draw the glyphs:

| Constant | Behavior |
|---|---|
| `cv2.LINE_4` | 4-connected line |
| `cv2.LINE_8` | 8-connected line (default) |
| `cv2.LINE_AA` | Anti-aliased line (smoother, recommended for readable overlays) |

### `bottomLeftOrigin` (optional, default `False`)
- Type: `bool`.
- If `True`, the image data origin is assumed to be at the bottom-left corner (flips text vertically) instead of the default top-left — rarely needed.

---

## Return Value

- Returns the same `image` array passed in (already modified in place); the return value is mainly for convenience/chaining.

---

## Basic Implementation Example

```python
import cv2

# 1. Load image
img = cv2.imread('frame.png')

# 2. Draw a simple label
cv2.putText(
    img,
    "Object Detected",
    (50, 50),                      # bottom-left corner of text
    cv2.FONT_HERSHEY_SIMPLEX,
    1.0,                            # font scale
    (0, 255, 0),                    # green
    2,                               # thickness
    cv2.LINE_AA
)

# 3. Example: label each detected contour with its area
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 500:
        continue
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(
        img,
        f"{area:.0f}px",
        (x, y - 10),                # just above the bounding box
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 0, 0),
        1,
        cv2.LINE_AA
    )

cv2.imshow('Labeled', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### Practical Notes

- `org` is the **bottom-left** of the text, not the top-left — if placing a label just above a bounding box, subtract a small offset from `y` (e.g., `y - 10`) so the text doesn't overlap the box.
- Use `cv2.getTextSize(text, fontFace, fontScale, thickness)` beforehand if you need to know the rendered text's width/height (e.g., to center it or draw a background rectangle behind it for readability).
- `cv2.LINE_AA` (anti-aliased) is recommended for any text meant to be read by a human (HUD overlays, debug labels); plain `LINE_8` is fine for text used only for masking/machine purposes (rare).
- Common in robotics/vision dashboards to overlay live telemetry (FPS, detected object counts, tag IDs, coordinates) directly onto the camera feed for on-screen debugging.
