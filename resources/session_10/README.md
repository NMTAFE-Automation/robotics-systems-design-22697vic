# Session 10

## Session Overview

- Investigation objective: build an autonomous behaviour loop with clear modes, priorities, and recovery steps.
- Robotics concept: behaviour hierarchies and robust autonomous operation.
- Expected behaviour: the system follows when safe, searches when the target is lost, avoids hazards, stops when needed, and recovers from failure conditions.

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

- OpenCV path: `cv2.cvtColor()`, `cv2.inRange()`, `cv2.findContours()`, `cv2.boundingRect()`, `cv2.putText()`
- Serial path: `serial.Serial()`, `ser.write()`
- HuskyLens equivalent path: `HuskyAdapter.get_object()`, `Maqueen.read_distance()`, `Maqueen.motor_stop_all()`

## Student Tasks

- define the behaviour modes
- build a hierarchy with safety at the top
- test automatic transitions
- add clear debugging output for active state changes

## Evidence Collection

- behaviour mode observations
- transition behaviour for target loss, target recovery, obstacle appearance, and obstacle removal
- notes about recovery and environmental robustness

## Troubleshooting References

- `session10/troubleshooting guide`
- `session10/cheatsheet`: `Troubleshooting Workflow`
- `session10/cheatsheet`: `Common Autonomous Behaviour Problems`

## Cheatsheet References

- `session10/cheatsheet`: `Behaviour Modes`
- `session10/cheatsheet`: `Behaviour Priorities`
- `session10/cheatsheet`: `Recovery Behaviour`

## Extension Challenges

- add a timed reverse step before recovery stop
- reduce false transitions with frame counters
- explain how the final hierarchy supports autonomous operation
