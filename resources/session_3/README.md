# Session 3

## Session Overview

- Investigation objective: understand images as matrices and test coordinate-based pixel operations.
- Robotics concept: digital perception foundations.
- Expected behaviour: students inspect frame shape, mark coordinates, read pixels, and convert to grayscale.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python 3
- OpenCV
- NumPy

## Library Functions Used

- `picamera2.Picamera2()`
- `cv2.circle()`
- `cv2.putText()`
- `cv2.cvtColor()`
- NumPy image slicing

## Student Tasks

- inspect `frame.shape`
- mark the image centre
- read one pixel in BGR order
- convert the live image to grayscale

## Evidence Collection

- recorded shape values
- coordinate behaviour observations
- notes about BGR versus grayscale

## Troubleshooting References

- `session3/troubleshooting guide`: `3. Vision Troubleshooting Workflow`
- `session3/troubleshooting guide`: `Problem 1 — Webcam Does Not Open`
- `session3/troubleshooting guide`: `Problem 3 — Blue/Red Colors Incorrect`

## Cheatsheet References

- `session3/cheatsheet`: `Image Shape`
- `session3/cheatsheet`: `Coordinate System`
- `session3/cheatsheet`: `Convert to Grayscale`

## Extension Challenges

- compare two camera resolutions
- edit a larger image region
- explain why grayscale simplifies later robot vision stages
