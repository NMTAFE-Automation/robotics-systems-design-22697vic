# Raspberry Pi → micro:bit → Maqueen

Control the Maqueen using camera images or typed commands.

## Colour commands versus target following

Both scripts use HSV (hue, saturation, brightness) to choose movement:

| Feature | [pi_camera_control.py](pi_camera_control.py) | [Session 8 target follower](../session08/lecturer_solution_opencv.py) |
| --- | --- | --- |
| Purpose | Colour selects movement | Follow a green target |
| Image analysis | Average colour of the whole image, including background | Filter for green pixels and find their outlines |
| Movement | Green → forward; blue → right; red → left | Target left → left; right → right; centre → forward |
| Stop | Dark image or unrecognised average colour | Target missing, too small, or very large |
| Decision | Most common command from the last five images | One command per image |
| Camera | Picamera2 | OpenCV `VideoCapture(0)` |

Only Session 8 follows an object's position and size.

Both send commands over USB serial at **115200 baud**, ending each with a newline. They send only when the command changes.

## Files

- `pi_send.py`: send typed movement commands from the Pi.
- `pi_camera_control.py`: move based on average image colour.
- `pi_colour_clasification_basic.py`: label one image's colour and save `classified_frame.jpg`; no movement commands.
- `main.py`: receive commands on the Maqueen's **micro:bit**; requires `maqueen.py`.

## Setup and run

Install on the Pi:

```bash
sudo apt install python3-serial python3-opencv python3-picamera2 -y
```

Load `main.py` and `maqueen.py` onto the micro:bit. Connect it to the Pi by USB and power the Maqueen. The scripts use `/dev/ttyACM0`.

From this folder, run one script at a time:

```bash
python3 pi_send.py
python3 pi_camera_control.py
python3 pi_colour_clasification_basic.py
```

## Commands

| Command | Action |
| --- | --- |
| `f` | Forward |
| `b` | Backward |
| `l` | Left |
| `r` | Right |
| `s` | Stop |
