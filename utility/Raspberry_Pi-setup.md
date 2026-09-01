# Raspberry Pi Setup Guide

## 0. Install Raspberry Pi OS on a Blank microSD Card

Use this section for brand new Raspberry Pi 4B units that do not have an operating system yet.

### What You Need

- a teacher or student laptop
- internet access
- a microSD card reader
- a microSD card for each Raspberry Pi

### Step 1: Download Raspberry Pi Imager

On the laptop, download and install Raspberry Pi Imager from the official Raspberry Pi site.

### Step 2: Insert the microSD Card

1. Insert the microSD card into the laptop.
2. Open Raspberry Pi Imager.

### Step 3: Choose the Operating System

For these activities, select:

```text
Raspberry Pi OS (64-bit)
```

This is the safest default for Raspberry Pi 4B classroom use with:

- `Picamera2`
- OpenCV
- Python 3
- serial communication

### Step 4: Choose the Storage Device

Select the correct microSD card in Raspberry Pi Imager.

Check carefully before writing, because the selected storage device will be erased.

### Step 5: Configure the Image Before Writing

Use the Raspberry Pi Imager settings option before writing the card.

Recommended settings:

- set a hostname such as `down-pi`
- set a username and password for the classroom
- configure Wi-Fi if the room uses wireless access
- set locale, keyboard layout, and timezone
- enable SSH if you want remote terminal access

Recommended classroom convention:

```text
Username: pi
Password: password1
```

Use a password your teaching team can manage consistently.

### Step 6: Write the Image

1. Click `Write`.
2. Wait for imaging and verification to finish.
3. Eject the microSD card safely.

### Step 7: First Boot

1. Insert the microSD card into the Raspberry Pi 4B.
2. Connect monitor, keyboard, mouse if available, and power.
3. Wait for the first boot to complete.

The first boot may take a few minutes while the system expands storage and completes setup.

### Step 8: Confirm the OS Installed Correctly

Open a terminal and run:

```bash
uname -a
python3 --version
```

If both commands work, the operating system is installed and ready for package setup.

### Step 9: Connect by SSH from Another Computer

If SSH was enabled in Raspberry Pi Imager, you can open a terminal on another computer and connect with:

```bash
ssh pi@down-pi.local
```

If `.local` hostname discovery does not work on your network, connect by IP address instead:

```bash
ssh pi@192.168.1.50
```

On the first connection:

1. type `yes` when asked to trust the host key
2. enter the Raspberry Pi password

After login, you can run normal Linux commands remotely, for example:

```bash
pwd
hostname
python3 --version
```

Create a working space folder in /home/pi directory called as "robotic_ws"

```bash
mkdir robotic_ws
```

To copy the course files from another computer (ex. session_3/ folder) to the Raspberry Pi, use `scp`:

```bash
scp -r session_3 pi@down-pi.local:/home/pi/robotic_ws
```

This gives students or teachers terminal access without needing a monitor connected to the Raspberry Pi.

## 1. Assemble the Hardware

1. Power the Raspberry Pi off.
2. Connect the Camera Module 3 ribbon cable to the Raspberry Pi camera port.
3. Make sure the metal contacts on the ribbon cable are seated correctly.
4. Connect monitor, keyboard, and power.
5. For robot-control sessions, connect the micro:bit to the Raspberry Pi by USB.

## 2. Boot Raspberry Pi OS

Use a current Raspberry Pi OS image.

After boot:

1. Open a terminal.
2. Update the package lists:

```bash
sudo apt update
```

3. Upgrade installed packages:

```bash
sudo apt full-upgrade -y
```

4. Reboot if prompted:

```bash
sudo reboot
```

## 3. Install Required Packages

Install the packages used by the activity files:

```bash
sudo apt install -y python3-opencv python3-picamera2 python3-serial
```

These cover:

- OpenCV image processing
- Picamera2 support for Camera Module 3
- serial communication to the micro:bit

## 4. Check the Camera

First confirm the camera is detected by the operating system:

```bash
rpicam-hello --list-cameras
```

You should see the Camera Module 3 listed.

Then run a basic preview test:

```bash
rpicam-hello
```

A "hello world"-equivalent for cameras, which starts a camera preview stream and displays it on the screen.

If the preview works, the camera is available to `Picamera2`.

## 5. Check Python Camera Access

Test `Picamera2` directly:

```bash
python3 -c "from picamera2 import Picamera2; cam = Picamera2(); cam.start(); print('camera ok'); cam.stop()"
```

If this prints `camera ok`, the Python camera path is ready.

## 6. Check OpenCV Imports

Test the Python packages:

```bash
python3 -c "import cv2, serial; from picamera2 import Picamera2; print(cv2.__version__)"
```

This should print an OpenCV version number without errors.

## 7. Copy or Open the Course Files

Open the repository folder on the Raspberry Pi and work from:

```text
~/home/pi/robotic_ws/session_3
```

The shared camera helper used by the OpenCV activities is:

```text
/common/pi_camera.py
```

This helper:

- prefers `Picamera2` for Raspberry Pi Camera Module 3
- falls back to OpenCV webcam capture only if needed on a non-Pi machine

## 8. Run an OpenCV Investigation

Example (working on folder for session 3):

```bash
cd /robotic_ws/session_3
python3 student_starter.py
```

Press `q` in the OpenCV window to close the activity.

## 9. Prepare the micro:bit Link for Sessions 8-10

The OpenCV robot-response sessions send single-letter commands to the micro:bit:

- `f` = forward
- `b` = backward
- `l` = left
- `r` = right
- `s` = stop

The repository already contains a matching micro:bit direction receiver at:

```text
maqueen_library/rasberrypi_firmware/microbit_direction_commands.py
```

Flash that program to the micro:bit before running Sessions 8-10 OpenCV activities.

## 10. Find the Serial Port

With the micro:bit plugged in, check the detected device:

```bash
ls /dev/ttyACM*
```

In many cases it will be:

```text
/dev/ttyACM0
```

If it is different, set the environment variable before running a robot-control session:

```bash
export MAQUEEN_SERIAL_PORT=/dev/ttyACM1
```

Then run the activity in the same terminal.

## 11. Run a Robot-Control Activity

Example (working on folder for session 11):

```bash
cd /robotic_ws/session_11
python3 student_starter.py
```

This requires:

- Camera Module 3 working
- micro:bit connected by USB
- Maqueen powered on
- the micro:bit receiver program already flashed

## 12. Safe Classroom Test Order

Use this order during setup:

1. test Raspberry Pi boot
2. test camera detection with `libcamera-hello`
3. test Python `Picamera2`
4. test OpenCV import
5. run Session 3 or Session 4 vision-only activity
6. flash the micro:bit receiver
7. confirm the serial port
8. run Session 8 robot-response activity in a clear test area

## 13. Troubleshooting

### Camera not detected

Check:

- ribbon cable orientation
- camera connector fully closed
- Raspberry Pi rebooted after reconnecting camera

Run:

```bash
libcamera-hello --list-cameras
```

### `picamera2` import fails

Reinstall the package:

```bash
sudo apt install -y python3-picamera2
```

### OpenCV windows do not appear

The activities use `cv2.imshow()`, so they need a graphical desktop session, VNC desktop, or connected monitor.

### Serial link to the micro:bit fails

Check:

- USB cable supports data, not power-only
- the micro:bit receiver program is flashed
- the correct `/dev/ttyACM*` device is selected

### Robot does not move in Sessions 8-10

Check:

- Maqueen battery connected
- micro:bit inserted correctly
- Maqueen powered on
- USB serial connection active
- the session is sending commands in the terminal output

## 14. Recommended First Classroom Run

If this is the first Pi setup, start with:

1. `robotic_ws/session_3/lecturer_solution.py`
2. `robotic_ws/session_4/lecturer_solution.py`
3. `robotic_ws/session_8/lecturer_solution_opencv.py`

That sequence verifies:

- camera capture
- OpenCV display
- image processing
- serial robot control
