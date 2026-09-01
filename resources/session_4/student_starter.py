import cv2
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 4 student scaffold.
# TODO: build a reticle, status text, and transparent overlay.

camera = open_camera()

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    overlay = frame.copy()
    height, width = frame.shape[:2]
    center_x = width // 2
    center_y = height // 2

    # TODO: draw a targeting reticle with lines and a centre marker.
    # TODO: add one rectangle and one text label.
    # TODO: blend the overlay back onto the camera feed with cv2.addWeighted().

    cv2.imshow("session04_student", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
