# Session 11

## Session Overview

- Investigation objective: use the existing integrated robot as a reference system while developing the Smart Warehouse design brief.
- Robotics concept: system architecture, subsystem responsibilities, and reuse planning.
- Expected behaviour: students observe how camera input becomes vision data, how vision data becomes decisions, and how serial commands become robot actions.

## Equipment Required

- computer
- Raspberry Pi with Pi Camera or a development machine with a webcam fallback
- Python
- OpenCV
- NumPy
- PySerial
- micro:bit
- Maqueen robot
- coloured target object
- coloured obstacle object

## Library Functions Used

- Canonical camera path: `open_camera()`, `read_frame()`, `close_camera()` from `code_activities_v1/common/pi_camera.py`
- OpenCV path: `cv2.cvtColor()`, `cv2.inRange()`, `cv2.findContours()`, `cv2.boundingRect()`, `cv2.putText()`, `cv2.imshow()`
- Serial path: `serial.Serial()`, `ser.write()`
- Existing robot command path: single-character `f`, `l`, `r`, `s` commands sent from Raspberry Pi to micro:bit to Maqueen

## Student Tasks

- RUN the existing integrated reference system
- OBSERVE the camera, vision, decision, serial, and robot-output stages
- IDENTIFY what the existing robot can already do
- IDENTIFY which Smart Warehouse job that capability could support
- IDENTIFY at least one current limitation of the existing system
- CONNECT reusable components and observed behaviour to the design brief
- CONNECT observed behaviour to a measurable success criterion

## Evidence Collection

- notes that support the worksheet sections on problem, users, jobs, limits, and success criteria

## Practical Alignment

- supports Investigation 1 by showing a real system that already solves a simpler movement problem
- supports Investigation 2 by helping students think about users who depend on safe robot behaviour
- supports Investigation 3 by making robot jobs visible through the existing command flow
- supports Investigation 4 by exposing limits such as colour dependence, camera view, and simple command outputs
- supports Investigation 5 by giving students concrete behaviours they can turn into measurable success criteria

## Assessment Preparation

- prepares students to draw a system diagram
- prepares students to identify reusable hardware and software
- prepares students to justify design choices for later prototype work
- does not provide a completed Smart Warehouse assessment solution
