import cv2
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 3 student scaffold.
# TODO: complete the coordinate marker, pixel read, and grayscale conversion tasks.

camera = open_camera()

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    height, width = frame.shape[:2]
    center_x = width // 2
    center_y = height // 2

    # TODO: draw a visible centre marker.
    # cv2.circle(...)

    # TODO: read the centre pixel and print the BGR values.

    # TODO: convert the frame to grayscale and show it in a second window.

    cv2.imshow("session03_student", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
