# Session 7

## Session Overview

- Investigation objective: track moving targets and analyse how position changes between frames.
- Robotics concept: tracking, bounding boxes, and centroids.
- Expected behaviour: students detect target regions, draw boxes, and interpret centroid motion.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- optional HuskyLens + Maqueen lecturer demonstration path

## Library Functions Used

- OpenCV path: `cv2.boundingRect()`, `cv2.contourArea()`, `cv2.circle()`
- HuskyLens path: `HuskyAdapter.get_result()`, `Maqueen.set_motor()`, `Maqueen.motor_stop_all()`

## Student Tasks

- rebuild the contour pipeline
- create stable tracking boxes
- calculate centroid coordinates
- compare slow and fast movement behaviour

## Evidence Collection

- tracking stability observations
- centroid behaviour under different motion styles
- notes about false tracking and lost targets

## Troubleshooting References

- `session7/troubleshooting guide`: `2. Tracking Troubleshooting Workflow`
- `session7/troubleshooting guide`: `Problem 1 — Tracking Flickers`
- `session7/troubleshooting guide`: `Problem 9 — Bounding Boxes Jump Around`

## Cheatsheet References

- `session7/cheatsheet`: `cv2.boundingRect()`
- `session7/cheatsheet`: `Centroids`
- `session7/cheatsheet`: `Drawing Tracking Information`

## Extension Challenges

- compare contour stability for slow and fast movement
- estimate whether larger boxes usually mean a closer target
- explain why stable preprocessing matters before tracking
