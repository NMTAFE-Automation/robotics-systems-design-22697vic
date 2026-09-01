import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 9 student scaffold.
# TODO: build a simple priority system where obstacle handling outranks target following.

camera = open_camera()
state = "STOP"
command = "s"

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    # TODO: create one mask for a target and one mask for an obstacle.
    # TODO: decide which condition has higher priority.
    # Recommended worksheet order:
    # 1. AVOID obstacle
    # 2. FOLLOW target
    # 3. SEARCH when target is lost
    # 4. STOP when no safe action is available
    print("state:", state, "command:", command)

    cv2.imshow("session09_student", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
