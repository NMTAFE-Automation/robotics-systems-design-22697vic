# Session 8

## Session Overview

- Investigation objective: follow a target by turning perception into robot movement decisions.
- Robotics concept: HSV tracking, centroid interpretation, and command-response workflows.
- Expected behaviour: a detected target on the left, right, or centre triggers the matching robot response.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- PySerial
- micro:bit
- Maqueen robot
- USB serial connection
- coloured target objects

## Library Functions Used

- OpenCV path: `cv2.cvtColor()`, `cv2.inRange()`, `cv2.findContours()`, `cv2.boundingRect()`
- Serial path: `serial.Serial()`, `ser.write()`
- HuskyLens equivalent path: `HuskyAdapter.get_object()`, `Maqueen.set_motor()`

## Student Tasks

- tune HSV colour thresholds
- isolate the target with a mask
- compute a centroid
- map target position to left, right, forward, or stop behaviour

## Evidence Collection

- HSV performance in different lighting
- target detection quality
- robot response observations for left, right, centre, near, and far targets

## Troubleshooting References

- `session8/troubleshooting guide`: `2. Interactive Robotics Troubleshooting Workflow`
- `session8/troubleshooting guide`: `Problem 1 — Wrong Color Tracked`
- `session8/troubleshooting guide`: `Problem 6 — Communication Fails`

## Cheatsheet References

- `session8/cheatsheet`: `Threshold Colors`
- `session8/cheatsheet`: `Centroids`
- `session8/cheatsheet.`: `Color Thresholding`

## Extension Challenges

- add a dead-band around the centre so the robot oscillates less
- compare simple and cluttered backgrounds
- explain why stable HSV masking matters before movement commands are sent
