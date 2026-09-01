import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 10 student scaffold.
# TODO: combine follow, search, avoid, stop, and recover modes into one loop.

camera = open_camera()

lost_frames = 0
mode = "STOP"
command = "s"

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    # TODO: create the target and obstacle masks.
    # TODO: set a behaviour hierarchy.
    # Suggested order for the worksheet:
    # 1. AVOID obstacle
    # 2. STOP if target is too close
    # 3. FOLLOW target
    # 4. SEARCH when target is lost
    # 5. RECOVER after repeated failures
    print("mode:", mode, "command:", command, "lost_frames:", lost_frames)

    cv2.imshow("session10_student", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
