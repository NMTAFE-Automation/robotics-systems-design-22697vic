import sys
import time
from pathlib import Path

import cv2
import numpy as np
import serial

LIBRARY_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(LIBRARY_ROOT / "common"))

from pi_camera import close_camera, open_camera, read_frame

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

TARGET_LOWER = np.array([40, 70, 70])
TARGET_UPPER = np.array([80, 255, 255])

OBSTACLE_LOWER_1 = np.array([0, 120, 70])
OBSTACLE_UPPER_1 = np.array([10, 255, 255])

OBSTACLE_LOWER_2 = np.array([170, 120, 70])
OBSTACLE_UPPER_2 = np.array([179, 255, 255])

MIN_TARGET_AREA = 600
MIN_OBSTACLE_AREA = 2500
TARGET_TOO_CLOSE_AREA = 18000

print("Session 11 system investigation")
print("Camera -> Vision -> Decision -> Serial -> Robot Output")
print("Press q to quit.\n")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

time.sleep(2)

camera_handle = open_camera()

last_command = None
last_state = None

try:
    while True:
        frame = read_frame(camera_handle)

        if frame is None:
            print("No frame received from camera.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        target_mask = cv2.inRange(hsv, TARGET_LOWER, TARGET_UPPER)

        obstacle_mask = cv2.inRange(hsv, OBSTACLE_LOWER_1, OBSTACLE_UPPER_1)

        obstacle_mask |= cv2.inRange(hsv, OBSTACLE_LOWER_2, OBSTACLE_UPPER_2)

        # default
        command = "s"
        state = "WAIT"

        capability_note = ("No strong target or obstacle detected.")

        # Detect a VALID red obstacle
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

        # Detect green target only if no valid obstacle
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

                    # Target too close
                    if target_area > TARGET_TOO_CLOSE_AREA:
                        state = "TARGET TOO CLOSE"
                        command = "s"

                        capability_note = ("Large target area triggers "
                                           "a safe stop.")
                    # Target left
                    elif cx < frame_center - 60:
                        state = "FOLLOW LEFT"
                        command = "l"

                        capability_note = ("Target is left of centre, "
                                           "so the robot turns left.")
                    # Target right
                    elif cx > frame_center + 60:
                        state = "FOLLOW RIGHT"
                        command = "r"

                        capability_note = ("Target is right of centre, "
                                           "so the robot turns right.")
                    # Target centred
                    else:
                        state = "FOLLOW FORWARD"
                        command = "f"

                        capability_note = ("Target is centred, "
                                           "so the robot moves forward.")
                else:
                    capability_note = ("Target was detected but too small "
                                       "for action.")

        if command != last_command:
            ser.write((command + "\n").encode())
            last_command = command

        if state != last_state:
            print("camera: frame captured")
            print("vision:", state)
            print("decision: command", command)
            print("target area:", int(target_area), "obstacle area:", int(obstacle_area))
            print("serial: sent", repr(command + "\n"))
            print("robot output:", capability_note)
            print("limitation: behaviour depends on "
                  "colour threshold and camera view\n")

            last_state = state

        cv2.putText(frame, f"STATE: {state}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, f"COMMAND: {command}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.putText(frame, "System stages: camera -> vision -> "
                           "decision -> serial -> robot", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (255, 255, 255), 2)

        cv2.imshow("session11_reference_system", frame)

        cv2.imshow("session11_target_mask", target_mask)

        cv2.imshow("session11_obstacle_mask", obstacle_mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    ser.write(b"s\n")
    ser.close()
    close_camera(camera_handle)
    cv2.destroyAllWindows()
