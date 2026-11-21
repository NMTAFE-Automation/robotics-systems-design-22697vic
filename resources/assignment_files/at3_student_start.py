# -----------------------------
# Assessment Task 3 – Multi-Colour System (STUDENT START CODE)
# HuskyLens (Color Recognition) -> Maqueen robot
#
# Before you start, on the HuskyLens:
#   1. Settings > Protocol Type = I2C
#   2. Select "Color Recognition"
#   3. Turn ON "Learn Multiple" (Color Recognition > Learn Multiple)
#   4. Learn the colours IN THIS ORDER:
#        ID 1 = RED     ID 2 = GREEN     ID 3 = BLUE
#
# Colour ID 1 (red)   -> stop
# Colour ID 2 (green) -> move forward
# Colour ID 3 (blue)  -> turn (one motor slower)
# No colour           -> stop safely
#
# Rename this file to main.py before flashing.
# Fill in every ______ line.
# -----------------------------
from maqueen import Maqueen
from huskyadapter import HuskyAdapter
from microbit import display
import utime

robot = Maqueen()
camera = HuskyAdapter(algorithm="color_recognition")

# -----------------------------
# STUDENT TASK 1:
# Complete the three movement functions.
# Hint: robot.set_motor(motor, speed)  and  robot.motor_stop_all()
# -----------------------------
def forward():
    # both motors same speed
    ______________________________
    ______________________________


def stop():
    # stop both motors
    ______________________________


def turn():
    # one motor faster, one motor slower
    ______________________________
    ______________________________


# -----------------------------
# STUDENT TASK 2:
# Light the two front RGB LEDs in the colour the robot can see.
# Hint: robot.rgb_front_left(red, green, blue)   values 0-255
#       robot.rgb_front_right(red, green, blue)
# -----------------------------
def show_colour(red, green, blue):
    ______________________________
    ______________________________


while True:
    # Read colour IDs from HuskyLens
    # ids is a LIST, e.g. []  or [2]  or  [3, 1]
    ids = camera.get_color_ids()

    # -----------------------------
    # STUDENT TASK 3:
    # Complete the logic below.
    # Hint: use  "number in ids"  to check if a colour is in the list.
    #       Do NOT use ids == 1  (a list is never equal to a number).
    # Think: which colour should be checked FIRST to keep the robot safe?
    # -----------------------------

    if ______ in ids:
        # red - stop
        ______________________________
        show_colour(______, ______, ______)
        display.show_________
        print(_________)
    elif ______ in ids:
        # green - move forward
        ______________________________
        show_colour(______, ______, ______)
        display.show_________
        print(_________)
    elif ______ in ids:
        # blue - turn (one motor slower)
        ______________________________
        show_colour(______, ______, ______)
        display.show_________
        print(_________)
    else:
        # no colour - stop safely, LEDs off
        ______________________________
        show_colour(0, 0, 0)
        display.show_________
        print(_________)

    # Delay 200 ms
    utime.sleep_ms(200)
