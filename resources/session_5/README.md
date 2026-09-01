# Session 5

## Session Overview

- Investigation objective: clean unreliable camera data before making decisions from it.
- Robotics concept: preprocessing pipelines.
- Expected behaviour: students compare raw, grayscale, blurred, thresholded, and morphology-cleaned images.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- NumPy

## Library Functions Used

- `cv2.cvtColor()`
- `cv2.GaussianBlur()`
- `cv2.medianBlur()`
- `cv2.threshold()`
- `cv2.adaptiveThreshold()`
- `cv2.morphologyEx()`

## Student Tasks

- display the raw feed
- convert to grayscale
- compare blur methods
- create a binary image
- clean the binary image with morphology

## Evidence Collection

- notes about shadows, reflections, and clutter
- binary image comparisons
- reliability observations after each preprocessing step

## Troubleshooting References

- `session5/troubleshooting guide`: `3. Preprocessing Troubleshooting Workflow`
- `session5/troubleshooting guide`: `Problem 3 — Binary Image Mostly White`
- `session5/troubleshooting guide`: `Problem 9 — Morphology Destroys Shapes`

## Cheatsheet References

- `session5/cheatsheet`: `cv2.GaussianBlur()`
- `session5/cheatsheet`: `cv2.threshold()`
- `session5/cheatsheet`: `Full Pipeline Example`

## Extension Challenges

- compare global and adaptive thresholding
- tune kernel size for morphology
- explain which stage improved reliability the most
