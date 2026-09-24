import serial
import time

# Connect to the micro:bit over USB at 115200 baud.
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
# Allow the connection to settle before sending commands.
time.sleep(2)

print("Manual control started")

while True:
    # Read a command: forward, backward, left, right, or stop.
    command = input("Enter command (f/b/l/r/s): ")
    # Send the text as bytes, ending with a newline for the receiver.
    ser.write((command + "\n").encode())
