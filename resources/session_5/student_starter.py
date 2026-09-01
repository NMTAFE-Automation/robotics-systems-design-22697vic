import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 5 student scaffold.
# TODO: build the preprocessing pipeline one stage at a time.

camera = open_camera()

kernel = np.ones((5, 5), np.uint8)

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    # TODO: convert to grayscale.
    gray = frame

    # TODO: test Gaussian and median blur.
    blurred = gray

    # TODO: create a binary image.
    binary = blurred

    # TODO: apply one morphology operation to improve reliability.
    cleaned = binary

    cv2.imshow("session05_student", cleaned)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
