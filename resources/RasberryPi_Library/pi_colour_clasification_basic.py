# Classify the average colour of one camera image and save it for inspection.
from picamera2 import Picamera2
import cv2
import time

# Start the Raspberry Pi camera and allow two seconds for it to warm up.
picam2 = Picamera2()
picam2.start()
time.sleep(2)

# Capture one image; treat it as BGRA and remove the alpha channel.
frame = picam2.capture_array()
frame_bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

# Separate colour (hue), colour intensity (saturation), and brightness (value).
hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

# Average all pixels, so the background also affects the classification.
avg_hue = hsv[:, :, 0].mean()
avg_sat = hsv[:, :, 1].mean()
avg_val = hsv[:, :, 2].mean()

# Check darkness and low colour intensity before testing colour ranges.
if avg_val < 50:
    label = "dark"
elif avg_sat < 40:
    label = "plain/grey"
# Red spans both ends of OpenCV's hue scale (0–179).
elif avg_hue < 15 or avg_hue > 165:
    label = "red"
elif 35 < avg_hue < 85:
    label = "green"
elif 90 < avg_hue < 130:
    label = "blue"
else:
    label = "unknown"

# Display the result and average hue to help interpret the classification.
print("Prediction:", label)
print("Hue:", round(avg_hue, 2))
print("Saved image test")

# Save the captured image in the current working directory, replacing any copy.
cv2.imwrite("classified_frame.jpg", frame_bgr)

# Stop the camera after this single-image test.
picam2.stop()
