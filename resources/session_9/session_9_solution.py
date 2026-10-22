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

# Session 9 lecturer reference solution with multi-condition priorities.

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
green_lower = np.array([40, 70, 70])  # TODO: tune for your target and lighting
green_upper = np.array([80, 255, 255])  # TODO: tune for your target and lighting

# First HSV range for red obstacle detection.
# Red appears at both ends of the HSV hue scale.
red_lower1 = np.array([0, 120, 70])
red_upper1 = np.array([10, 255, 255])

# Second HSV range for red obstacle detection.
red_lower2 = np.array([170, 120, 70])
red_upper2 = np.array([179, 255, 255])

# Store the previous command to avoid repeatedly sending the same command.
last_command = None
# Store the previous state so the console prints every state change.
last_state = None

# Kernel for removing small specks from the masks. (Option)
kernel = np.ones((5, 5), np.uint8)

# Main camera and robot control loop.
while True:

    # Capture one frame from the camera.
    frame = read_frame(camera)

    # Stop the loop if the camera fails to return a frame.
    if frame is None:
        break

    # Convert the image from BGR to HSV colour space.
    # HSV makes colour filtering easier and more reliable.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a binary mask for the green target.
    # White pixels represent areas matching the green range.
    target_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Create a binary mask for red obstacles.
    # The two red ranges are combined using OR.
    obstacle_mask = cv2.inRange(hsv, red_lower1, red_upper1) | cv2.inRange(hsv, red_lower2, red_upper2)

    # Remove small specks (noise) from both masks. (option)
    target_mask = cv2.morphologyEx(target_mask, cv2.MORPH_OPEN, kernel)
    obstacle_mask = cv2.morphologyEx(obstacle_mask, cv2.MORPH_OPEN, kernel)

    # Default command is stop.
    command = "s"

    # Default displayed behaviour state.
    state = "STOP"

    # flag for a real obstacle
    obstacle_found = False

    # Find contours in the red obstacle mask.
    # Obstacles are checked first because avoidance has priority.
    obstacle_contours, _ = cv2.findContours(obstacle_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If any red obstacle regions are detected, process them first.
    if obstacle_contours:

        # Select the largest red obstacle region.
        obstacle = max(obstacle_contours, key=cv2.contourArea)

        # Only react to obstacles larger than the noise threshold.
        if cv2.contourArea(obstacle) > 2500:

            # Calculate a bounding rectangle around the obstacle.
            x, y, w, h = cv2.boundingRect(obstacle)

            # Draw a red box around the obstacle on the display frame.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Set the robot to turn left to avoid the obstacle.
            command = "l"

            # Update the state label to show avoidance is active.
            state = "AVOID PRIORITY"

            # set only for a big red area
            obstacle_found = True

    # Only look for the target if no large obstacle was found.
    if not obstacle_found:

        # Find contours in the green target mask.
        target_contours, _ = cv2.findContours(target_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If green target regions are detected, process the largest one.
        if target_contours:

            # Select the largest green target region.
            target = max(target_contours, key=cv2.contourArea)
        else:
            target = None

        if target is not None and cv2.contourArea(target) > 600:  # Ignore small green regions that are likely noise.

            # Calculate a bounding rectangle around the target.
            x, y, w, h = cv2.boundingRect(target)

            # Calculate the horizontal centre of the target.
            cx = x + w // 2

            # Draw a green box around the target.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, str(int(cv2.contourArea(target))), (x, max(20, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # If the target is left of the frame centre, turn left.
            if cx < frame.shape[1] // 2 - 60:
                command = "l"
                state = "FOLLOW LEFT"

            # If the target is right of the frame centre, turn right.
            elif cx > frame.shape[1] // 2 + 60:
                command = "r"
                state = "FOLLOW RIGHT"

            # If the target is close to the centre, drive forward.
            else:
                command = "f"
                state = "FOLLOW CENTRE"

        # If no target is detected, rotate/search.
        else:
            command = "r"
            state = "SEARCH / WAIT"

    # Send a command only when it changes.
    if command != last_command:

        # Send the command string to the micro:bit/Maqueen.
        ser.write((command + "\n").encode())

        # Store the command so it is not resent unnecessarily.
        last_command = command

    # Print the state whenever it changes (even if the command is the same).
    if state != last_state:
        print("state:", state, "command:", command)
        last_state = state

    # Draw the current robot state on the camera frame.
    cv2.putText(frame, state, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show the camera frame with overlays.
    cv2.imshow("session09_multi_behaviour", frame)

    # Show the green target binary mask.
    cv2.imshow("session09_target_mask", target_mask)

    # Show the red obstacle binary mask.
    cv2.imshow("session09_obstacle_mask", obstacle_mask)

    # Press q to quit.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Send a final stop command before shutdown.
ser.write(b"s\n")

# Release the camera.
close_camera(camera)

# Close all OpenCV windows.
cv2.destroyAllWindows()
