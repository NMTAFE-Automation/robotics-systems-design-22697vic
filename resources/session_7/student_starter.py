import cv2
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
from pi_camera import close_camera, open_camera, read_frame

# Session 7 student scaffold.
# TODO: build a stable tracking pipeline with contours, bounding boxes, and centroids.

camera = open_camera()
kernel = np.ones((5, 5), np.uint8)
last_centroid = None

while True:
    frame = read_frame(camera)
    if frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # TODO: rebuild the Session 6 preprocessing pipeline:
    # 1. blur the grayscale image
    # 2. threshold it into a binary image
    # 3. clean it with morphology
    processed = gray

    # TODO: find contours from the processed image.
    contours = []

    display = frame.copy()
    for contour in contours:
        # TODO: filter small contours.
        # TODO: add a bounding box and centroid marker.
        # TODO: compare the current centroid with last_centroid to describe movement.
        pass

    cv2.imshow("session07_student", display)
    cv2.imshow("session07_processed", processed)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

close_camera(camera)
cv2.destroyAllWindows()
