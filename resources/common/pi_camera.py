import time

import cv2


def open_camera(size=(640, 480), warmup_seconds=2.0, fallback_index=0):
    """
    Open the preferred classroom camera source.

    Priority order:
    1. Raspberry Pi Camera Module via Picamera2
    2. OpenCV webcam fallback for development machines
    """
    try:
        from picamera2 import Picamera2

        camera = Picamera2()
        config = camera.create_preview_configuration(
            main={"format": "XRGB8888", "size": size}
        )
        camera.configure(config)
        camera.start()
        time.sleep(warmup_seconds)
        return {"backend": "picamera2", "camera": camera}
    except Exception:
        cap = cv2.VideoCapture(fallback_index)
        if not cap.isOpened():
            raise RuntimeError(
                "Camera did not open. Check that Picamera2 is installed or a webcam is connected."
            )
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        return {"backend": "opencv", "camera": cap}


def read_frame(camera_handle):
    """Read one BGR frame regardless of the underlying camera backend."""
    if camera_handle["backend"] == "picamera2":
        frame = camera_handle["camera"].capture_array()
        if frame is None:
            return None
        if len(frame.shape) == 3 and frame.shape[2] == 4:
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        if len(frame.shape) == 2:
            return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        return frame

    ok, frame = camera_handle["camera"].read()
    if not ok:
        return None
    return frame


def close_camera(camera_handle):
    """Release either Picamera2 or OpenCV camera resources."""
    if camera_handle["backend"] == "picamera2":
        camera_handle["camera"].stop()
    else:
        camera_handle["camera"].release()
