import sys
import time
from pathlib import Path

import cv2
import numpy as np
import serial

LIBRARY_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(LIBRARY_ROOT / "common"))

from pi_camera import close_camera, open_camera, read_frame

# =========================================================
# SESSION 11 STUDENT REFERENCE SYSTEM
# Smart Warehouse Design Brief - System Investigation
#
# PURPOSE:
# Use the existing working robot as a reference system
# while you write your Smart Warehouse design brief.
#
# This is NOT a "build a new controller" exercise.
# Run the system and observe how each stage works:
#
#   camera -> vision -> decision -> serial -> robot output
#
# Then use what you observe in Investigations 1-5:
# problem, users, robot jobs, limits and success criteria.
# =========================================================

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

# Green target HSV range
# (in the Smart Warehouse: a pickup bay or parcel marker)
TARGET_LOWER = np.array([40, 70, 70])
TARGET_UPPER = np.array([80, 255, 255])

# Red obstacle HSV ranges
# (in the Smart Warehouse: a person, forklift or hazard)
# Red sits at both ends of the HSV hue scale, so two ranges are needed.
OBSTACLE_LOWER_1 = np.array([0, 120, 70])
OBSTACLE_UPPER_1 = np.array([10, 255, 255])

OBSTACLE_LOWER_2 = np.array([170, 120, 70])
OBSTACLE_UPPER_2 = np.array([179, 255, 255])

# Detection thresholds (contour area in pixels)
MIN_TARGET_AREA = 600  # smaller green regions are treated as noise
MIN_OBSTACLE_AREA = 2500  # smaller red regions are treated as noise
TARGET_TOO_CLOSE_AREA = 18000  # target this big means the robot is close enough

print("Session 11 student system investigation")
print("Use the existing robot to support your Smart Warehouse design brief.")
print("System stages: camera -> vision -> decision -> serial -> robot output")
print("Press q to quit.\n")

print("INVESTIGATION QUESTIONS")
print("1. What can the existing robot already do?")
print("2. Which warehouse users depend on safe robot behaviour?")
print("3. Which Smart Warehouse job could each behaviour support?")
print("4. What is at least one limitation of the current system?")
print("5. How could you measure success for one observed behaviour?\n")

# ---------------------------------------------------------
# Open serial connection and camera
# ---------------------------------------------------------

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Give the micro:bit time to get ready after the port opens.
time.sleep(2)

camera_handle = open_camera()

# Remember the last command and state so we only react to changes.
last_command = None
last_state = None

# Kernel for removing small specks from the masks. (Option)
kernel = np.ones((5, 5), np.uint8)

try:
    while True:
        # =================================================
        # CAMERA STAGE
        #
        # Capture one image from the Pi camera.
        # =================================================

        frame = read_frame(camera_handle)

        if frame is None:
            print("No frame received from camera.")
            break

        # =================================================
        # VISION STAGE
        #
        # Convert the image to HSV and make two black/white
        # masks: white pixels = matching colour.
        # Watch the mask windows while the robot runs.
        # =================================================

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        target_mask = cv2.inRange(hsv, TARGET_LOWER, TARGET_UPPER)

        obstacle_mask = cv2.inRange(hsv, OBSTACLE_LOWER_1, OBSTACLE_UPPER_1) | cv2.inRange(hsv, OBSTACLE_LOWER_2, OBSTACLE_UPPER_2)

        # Remove small specks (noise) from both masks. (Option)
        target_mask = cv2.morphologyEx(target_mask, cv2.MORPH_OPEN, kernel)
        obstacle_mask = cv2.morphologyEx(obstacle_mask, cv2.MORPH_OPEN, kernel)

        # =================================================
        # DEFAULT DECISION
        #
        # If nothing valid is seen, the robot waits (stops).
        # =================================================

        command = "s"
        state = "WAIT"

        capability_note = ("No strong target or obstacle detected.")

        # =================================================
        # PRIORITY 1: VALID RED OBSTACLE
        #
        # Safety comes first, so the obstacle is checked
        # before the target.
        #
        # Important:
        # A tiny red contour does NOT count as a valid obstacle.
        # Only a contour larger than MIN_OBSTACLE_AREA should
        # stop the robot.
        # =================================================

        obstacle_detected = False
        obstacle_area = 0

        obstacle_contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if obstacle_contours:
            obstacle = max(obstacle_contours, key=cv2.contourArea)

            obstacle_area = cv2.contourArea(obstacle)

            if obstacle_area > MIN_OBSTACLE_AREA:
                x, y, w, h = cv2.boundingRect(obstacle)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                state = "OBSTACLE PRIORITY"
                command = "s"

                capability_note = ("Red obstacle forces a stop command.")

                obstacle_detected = True

        # =================================================
        # PRIORITY 2: GREEN TARGET
        #
        # Target detection runs only when there is no VALID
        # obstacle. Small red noise therefore does not prevent
        # the green target from being evaluated.
        #
        # Order of checks:
        #   too close -> stop
        #   left of centre -> turn left
        #   right of centre -> turn right
        #   centred -> move forward
        # =================================================

        target_area = 0

        if not obstacle_detected:
            target_contours, _ = cv2.findContours(target_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if target_contours:
                target = max(target_contours, key=cv2.contourArea)

                target_area = cv2.contourArea(target)

                if target_area > MIN_TARGET_AREA:
                    x, y, w, h = cv2.boundingRect(target)

                    cx = x + w // 2
                    cy = y + h // 2

                    frame_center = (frame.shape[1] // 2)

                    # Draw target box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Draw target centre
                    cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

                    # -------------------------------------
                    # Target too close
                    # -------------------------------------
                    if target_area > TARGET_TOO_CLOSE_AREA:
                        state = "TARGET TOO CLOSE"
                        command = "s"

                        capability_note = ("Large target area triggers "
                                           "a safe stop.")

                    # -------------------------------------
                    # Target left
                    # (60 pixels either side of centre is a
                    # "dead zone" to stop left/right wobble)
                    # -------------------------------------
                    elif cx < frame_center - 60:
                        state = "FOLLOW LEFT"
                        command = "l"

                        capability_note = ("Target is left of centre, "
                                           "so the robot turns left.")

                    # -------------------------------------
                    # Target right
                    # -------------------------------------
                    elif cx > frame_center + 60:
                        state = "FOLLOW RIGHT"
                        command = "r"

                        capability_note = ("Target is right of centre, "
                                           "so the robot turns right.")

                    # -------------------------------------
                    # Target centred
                    # -------------------------------------
                    else:
                        state = "FOLLOW FORWARD"
                        command = "f"

                        capability_note = ("Target is centred, "
                                           "so the robot moves forward.")

                # -------------------------------------
                # Green seen, but too small to act on
                # -------------------------------------
                else:
                    capability_note = ("Target was detected but too small "
                                       "for action.")

        # =================================================
        # SERIAL STAGE
        #
        # Send a single-character command to the micro:bit:
        #   f = forward, l = left, r = right, s = stop
        # A command is only sent when it changes.
        # =================================================

        if command != last_command:
            ser.write((command + "\n").encode())
            last_command = command

        # =================================================
        # OBSERVATION / EVIDENCE
        #
        # This printout appears only when the state changes.
        # Use these values as evidence in the worksheet.
        # Do not simply copy the message as your answer.
        # Explain what the observed behaviour means for your
        # Smart Warehouse design brief.
        # =================================================

        if state != last_state:
            print("camera: frame captured")
            print("vision:", state)
            print("decision: command", command)
            print("target area:", int(target_area), "obstacle area:", int(obstacle_area))
            print("serial: sent", repr(command + "\n"))
            print("robot output:", capability_note)
            print("limitation: behaviour depends on "
                  "colour threshold and camera view")

            print("student task: link this behaviour to a warehouse job, "
                  "a limitation or a success criterion.\n")

            last_state = state

        # =================================================
        # DISPLAY
        # =================================================

        cv2.putText(frame, f"STATE: {state}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, f"COMMAND: {command}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, "System stages: camera -> vision -> "
                           "decision -> serial -> robot", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (255, 255, 255), 2)

        cv2.imshow("session11_student_reference_system", frame)

        cv2.imshow("session11_target_mask", target_mask)

        cv2.imshow("session11_obstacle_mask", obstacle_mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    # =====================================================
    # SAFE SHUTDOWN
    #
    # Always send stop and release the hardware,
    # even if the program crashes or you press Ctrl+C.
    # =====================================================

    ser.write(b"s\n")
    ser.close()

    close_camera(camera_handle)

    cv2.destroyAllWindows()
