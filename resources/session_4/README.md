# Session 4

## Session Overview

- Investigation objective: create overlays that help operators understand robot vision and system state.
- Robotics concept: HUD systems and visual debugging.
- Expected behaviour: students draw lines, circles, rectangles, text, and transparent layers onto live video.

## Equipment Required

- Raspberry Pi 4B
- Raspberry Pi Camera Module 3
- Python
- OpenCV
- NumPy

## Library Functions Used

- `cv2.line()`
- `cv2.circle()`
- `cv2.rectangle()`
- `cv2.putText()`
- `cv2.addWeighted()`

## Student Tasks

- build a targeting reticle
- add one status panel
- test line thickness, colour, and target size
- explain why overlays help debugging

## Evidence Collection

- overlay comparisons
- reticle alignment notes
- transparency observations

## Troubleshooting References

- `session4/troubleshooting guide`: `3. Overlay Troubleshooting Workflow`
- `session4/troubleshooting guide`: `Problem 1 — Shapes Not Visible`
- `session4/troubleshooting guide`: `Problem 6 — Raw Camera Feed Destroyed`

## Cheatsheet References

- `session4/cheatsheet`: `cv2.line()`
- `session4/cheatsheet`: `cv2.addWeighted()`
- `session4/cheatsheet`: `Common HUD Elements`

## Extension Challenges

- add a moving scanner line
- display live frame dimensions
- design a more readable warning panel
