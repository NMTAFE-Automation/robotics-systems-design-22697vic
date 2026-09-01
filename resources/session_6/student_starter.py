import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 6 student scaffold.
# TODO: rebuild the preprocessing pipeline and then isolate useful contours.

camera = open_camera()

kernel = np.ones((5, 5), np.uint8)

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    # TODO: convert the frame to a cleaned binary image.
    cleaned = frame

    # TODO: call cv2.findContours() on the cleaned image.
    contours = []

    display = frame.copy()
    for contour in contours:
        # TODO: ignore very small contours.
        # TODO: draw the contour and bounding box.
        pass

    cv2.imshow("session06_student", display)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
