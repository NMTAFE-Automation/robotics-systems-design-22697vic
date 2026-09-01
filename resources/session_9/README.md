# Session 9

## Session Overview

- Investigation objective: combine multiple conditions into one behaviour system with clear priorities.
- Robotics concept: decision layers and behaviour switching.
- Expected behaviour: the robot follows a target when safe, but stops or avoids when a higher-priority obstacle condition appears.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- PySerial
- micro:bit
- Maqueen robot
- coloured target objects
- obstacles

## Library Functions Used

- OpenCV path: `cv2.inRange()`, `cv2.findContours()`, `cv2.boundingRect()`, `cv2.putText()`
- Serial path: `serial.Serial()`, `ser.write()`
- HuskyLens equivalent path: `HuskyAdapter.get_object()`, `Maqueen.read_distance()`, `Maqueen.set_motor()`

## Student Tasks

- detect at least two conditions
- define a behaviour-priority order
- observe behaviour switching
- show the active state clearly while testing

## Evidence Collection

- behaviour under target-only, obstacle-only, both, and no-condition cases
- notes about unstable switching
- environmental effects on the final decision

## Troubleshooting References

- `session9/troubleshooting guide`: `2. Intelligent Robotics Troubleshooting Workflow`
- `session9/troubleshooting guide`: `Problem 2 — Robot Ignores Obstacles`
- `session9/troubleshooting guide`: `Problem 8 — Behaviour Switching Too Fast`

## Cheatsheet References

- `session9/cheatsheet`: `Behaviour Priorities`
- `session9/cheatsheet`: `Obstacle Vs Target`
- `session9/cheatsheet`: `Decision Visibility`

## Extension Challenges

- add a real search mode instead of waiting
- reduce oscillation between states
- explain why obstacle avoidance usually outranks target following
