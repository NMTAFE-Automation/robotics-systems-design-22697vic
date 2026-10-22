import cv2
import numpy as np
import os
import serial
import time
from pathlib import Path
import sys

# Add the shared "common" folder to Python's search path
# so the camera helper functions can be imported.
sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))

# Import helper functions for opening, reading from, and closing the camera.
from pi_camera import close_camera, open_camera, read_frame

# Session 10 lecturer reference solution with behaviour modes and recovery logic.
# Builds on the Session 9 multi-condition priority solution.
#
# Behaviour hierarchy (highest priority first):
#   1. AVOID         - large red obstacle in view
#   2. ARRIVED STOP  - green target is very close
#   3. FOLLOW        - green target visible (LEFT / RIGHT / CENTRE)
#   4. SEARCH        - target lost for a short time
#   5. RECOVER       - target lost for longer, reverse to make space

# Read the Maqueen serial port from an environment variable.
# If the variable is not set, use /dev/ttyACM0 as the default port.
SERIAL_PORT = os.environ.get("MAQUEEN_SERIAL_PORT", "/dev/ttyACM0")

# Open a serial connection to the micro:bit/Maqueen controller.
ser = serial.Serial(SERIAL_PORT, 115200, timeout=1)

# Allow time for the serial connection to initialise.
time.sleep(2)

# Open the Raspberry Pi camera.
camera = open_camera()

# HSV colour range for the green target object.
green_lower = np.array([35, 50, 50])  # TODO: tune for your target and lighting
green_upper = np.array([85, 255, 255])  # TODO: tune for your target and lighting


# First HSV range for red obstacle detection.
# Red appears at both ends of the HSV hue scale.
red_lower1 = np.array([0, 120, 70])  # TODO: tune for your obstacles and lighting
red_upper1 = np.array([10, 255, 255])

# Second HSV range for red obstacle detection.
red_lower2 = np.array([170, 120, 70])  # TODO: tune for your obstacles and lighting
red_upper2 = np.array([179, 255, 255])

# Area thresholds (in pixels).
OBSTACLE_MIN_AREA = 2500  # TODO: smaller value = react to obstacles further away
TARGET_MIN_AREA = 600  # TODO: ignore green regions smaller than this (noise)
TARGET_STOP_AREA = 18000  # TODO: target this big means the robot has arrived

# Dead zone either side of the frame centre (in pixels).
CENTRE_DEADBAND = 60  # TODO: larger value = less left/right wobble

# Lost-target frame limits.
SEARCH_FRAMES = 15  # TODO: frames to spin and search before recovering

# Store the previous command to avoid repeatedly sending the same command.
last_command = None

# Store the previous mode so mode changes can be printed.
last_mode = None

# Count how many frames the robot has gone without seeing a valid target.
# This drives the SEARCH -> RECOVER sequence.
lost_frames = 0

# Kernel for removing small specks from the masks. (Option)
kernel = np.ones((5, 5), np.uint8)

# Main camera and robot control loop.
while True:

    # Capture one frame from the camera.
    frame = read_frame(camera)

    # Stop the loop if the camera fails to return a frame.
    if frame is None:
        break

    # Calculate the horizontal centre of the camera frame.
    frame_center = frame.shape[1] // 2

    # Convert the image from BGR to HSV colour space.
    # HSV makes colour filtering easier and more reliable.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a binary mask for the green target.
    # White pixels represent areas matching the green range.
    target_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Create a binary mask for red obstacles.
    # The two red ranges are combined using OR.
    obstacle_mask = cv2.inRange(hsv, red_lower1, red_upper1) | cv2.inRange(hsv, red_lower2, red_upper2)

    # Remove small specks (noise) from both masks. (Option)
    target_mask = cv2.morphologyEx(target_mask, cv2.MORPH_OPEN, kernel)
    obstacle_mask = cv2.morphologyEx(obstacle_mask, cv2.MORPH_OPEN, kernel)

    # Default command is stop.
    command = "s"

    # Default behaviour mode.
    mode = "STOP"

    # Flag for a real (large) obstacle.
    obstacle_found = False

    # ---------- Priority 1: obstacle avoidance ----------

    # Find contours in the red obstacle mask.
    # Obstacles are checked first because avoidance has the highest priority.
    obstacle_contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If any red obstacle regions are detected, process the largest one.
    if obstacle_contours:

        # Select the largest red obstacle region.
        obstacle = max(obstacle_contours, key=cv2.contourArea)

        # Only react to obstacles larger than the noise threshold.
        if cv2.contourArea(obstacle) > OBSTACLE_MIN_AREA:

            # Calculate a bounding rectangle around the obstacle.
            x, y, w, h = cv2.boundingRect(obstacle)

            # Draw a red box around the obstacle on the display frame.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Turn left to avoid the obstacle.
            command = "l"
            mode = "AVOID"

            # Set only for a big red area.
            obstacle_found = True

            # Reset the lost-frame count because the robot is busy avoiding.
            lost_frames = 0

    # ---------- Priorities 2 and 3: arrive or follow the target ----------

    # Only look for the target if no large obstacle was found.
    if not obstacle_found:

        # Find contours in the green target mask.
        target_contours, _ = cv2.findContours(target_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If green target regions are detected, select the largest one.
        if target_contours:
            target = max(target_contours, key=cv2.contourArea)
        else:
            target = None

        # Ignore small green regions that are likely noise.
        if target is not None and cv2.contourArea(target) > TARGET_MIN_AREA:

            # Reset the lost-frame count because a valid target was found.
            lost_frames = 0

            # Calculate the target area.
            area = cv2.contourArea(target)

            # Calculate a bounding rectangle around the target.
            x, y, w, h = cv2.boundingRect(target)

            # Calculate the centre of the target.
            cx = x + w // 2
            cy = y + h // 2

            # Draw a green box, the area value, and a red centre dot.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, str(int(area)), (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

            # If the target is very large, the robot has arrived - stop.
            if area > TARGET_STOP_AREA:
                command = "s"
                mode = "ARRIVED STOP"

            # If the target is left of the frame centre, turn left.
            elif cx < frame_center - CENTRE_DEADBAND:
                command = "l"
                mode = "FOLLOW LEFT"

            # If the target is right of the frame centre, turn right.
            elif cx > frame_center + CENTRE_DEADBAND:
                command = "r"
                mode = "FOLLOW RIGHT"

            # If the target is close to the centre, drive forward.
            else:
                command = "f"
                mode = "FOLLOW CENTRE"

        # ---------- Priorities 4 and 5: search and recover ----------

        # No valid target this frame.
        else:

            # Count one more frame without a target.
            lost_frames += 1

            # Short loss: rotate on the spot to search for the target.
            if lost_frames < SEARCH_FRAMES:
                command = "r"
                mode = "SEARCH"

            # Longer loss: reverse to make space.
            else:
                command = "b"
                mode = "RECOVER"

    # Send a command only when it changes.
    if command != last_command:

        # Send the command string to the micro:bit/Maqueen.
        ser.write((command + "\n").encode())

        # Store the command so it is not resent unnecessarily.
        last_command = command

    # Print a debug line only when the behaviour mode changes.
    if mode != last_mode:
        print("mode:", last_mode, "->", mode, "| command:", command, "| lost_frames:", lost_frames)
        last_mode = mode

    # Draw the current behaviour mode and lost-frame count on the camera frame.
    cv2.putText(frame, mode, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, "lost: " + str(lost_frames), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show the camera frame with overlays.
    cv2.imshow("session10_autonomous_robot", frame)

    # Show the green target binary mask.
    cv2.imshow("session10_target_mask", target_mask)

    # Show the red obstacle binary mask.
    cv2.imshow("session10_obstacle_mask", obstacle_mask)

    # Press q to quit.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Send a final stop command before shutdown.
ser.write(b"s\n")

# Release the camera.
close_camera(camera)

# Close all OpenCV windows.
cv2.destroyAllWindows()
