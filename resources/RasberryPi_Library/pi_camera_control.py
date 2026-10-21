# Use the camera's average colour to choose and send Maqueen movement commands.
from picamera2 import Picamera2
import cv2
import time
import serial
from collections import deque, Counter

# Opens a serial connection to the micro:bit over USB
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # Allow time for connection to stabilise

# Start the Raspberry Pi camera before capturing images.
picam2 = Picamera2()
picam2.start()
time.sleep(2)  # Allow camera sensor to warm up

print("Running smoothed camera control...")

# Keep the latest five decisions; older entries are dropped automatically.
command_buffer = deque(maxlen=5)

# Track the last command sent to avoid repeated sending
last_sent_command = None

while True:
    # Capture a single frame from the camera
    frame = picam2.capture_array()

    # Treat the captured image as BGRA and remove its alpha channel for processing.
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Separate colour (hue), colour intensity (saturation), and brightness (value).
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Average all pixels, so the background also affects the colour decision.
    avg_hue = hsv[:, :, 0].mean()  # Colour type (0–179)
    avg_sat = hsv[:, :, 1].mean()  # Colour intensity (not used in decisions below)
    avg_val = hsv[:, :, 2].mean()  # Brightness


    # Stop for dark images; otherwise map average hue to a movement command.
    if avg_val < 50:
        command = 's'   # Very dark → STOP

    elif 35 < avg_hue < 85:
        command = 'f'   # Green → FORWARD

    elif 90 < avg_hue < 130:
        command = 'r'   # Blue → TURN RIGHT

    elif avg_hue < 15 or avg_hue > 165:
        command = 'l'   # Red → TURN LEFT

    else:
        command = 's'   # Unknown → STOP

    # Add the current decision to the buffer
    command_buffer.append(command)

    # Wait for five samples, then reconsider the latest five on every loop.
    if len(command_buffer) == command_buffer.maxlen:

        # Choose the most frequent command to reduce brief colour fluctuations.
        most_common = Counter(command_buffer).most_common(1)[0][0]

        # Only send command if it has changed
        if most_common != last_sent_command:

            print(f"Stable Command: {most_common} (Hue: {avg_hue:.2f})")

            # Send the letter as bytes with a newline for the micro:bit's readline().
            ser.write((most_common + "\n").encode())

            # Update last sent command
            last_sent_command = most_common

    # Pause 0.2 seconds between decisions (capture and processing add extra time).
    time.sleep(0.2)
