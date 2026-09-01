import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 8 student scaffold.
# TODO: isolate a target colour, find its centroid, and choose left/right/forward commands.

camera = open_camera()

lower = np.array([40, 70, 70])
upper = np.array([80, 255, 255])
command = "s"

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    # TODO: convert to HSV and build a mask for the target colour.
    mask = frame[:, :, 0]

    # TODO: detect contours and ignore very small targets.
    contours = []

    # TODO: compute a centroid and decide between left, right, forward, or stop.
    # Suggested worksheet mapping:
    # target left -> command = "l"
    # target right -> command = "r"
    # target centre -> command = "f"
    # no target or very close target -> command = "s"
    print("command:", command)

    cv2.imshow("session08_student", frame)
    cv2.imshow("session08_mask", mask)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
