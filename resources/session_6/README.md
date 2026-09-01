# Session 6

## Session Overview

- Investigation objective: detect object boundaries and isolate useful shapes.
- Robotics concept: contour detection and target regions.
- Expected behaviour: students clean the image, find contours, filter small regions, and draw bounding boxes.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- NumPy

## Library Functions Used

- `cv2.findContours()`
- `cv2.drawContours()`
- `cv2.boundingRect()`
- `cv2.contourArea()`
- `cv2.morphologyEx()`

## Student Tasks

- rebuild the Session 5 pipeline
- detect contours
- compare large and small regions
- add contour and box overlays

## Evidence Collection

- contour quality observations
- notes about different backgrounds and lighting
- comparison of filtered and unfiltered results

## Troubleshooting References

- `session6/troubleshooting guide`: `2. Contour Troubleshooting Workflow`
- `session6/troubleshooting guide`: `Problem 1 — Too Many Contours`
- `session6/troubleshooting guide`: `Problem 4 — Bounding Boxes Flicker`

## Cheatsheet References

- `session6/cheatsheet`: `cv2.findContours()`
- `session6/cheatsheet`: `cv2.boundingRect()`
- `session6/cheatsheet`: `Area Filtering Quick Reference`

## Extension Challenges

- compare contour behaviour on different objects
- tune the area threshold
- explain why cleaned binary images improve contour reliability
