# -----------------------------
# Assessment Task 2 – Multi-Tag System (STUDENT START CODE)
# HuskyLens (Tag Recognition) -> Maqueen robot
#
# Tag 1  -> move forward
# Tag 2  -> stop
# Tag 3  -> turn (one motor slower)
# No tag -> stop safely
#
# Fill in every ______ line.
# -----------------------------
from maqueen import Maqueen
from huskyadapter import HuskyAdapter
from microbit import display
import utime

robot = Maqueen()
camera = HuskyAdapter()

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


while True:
    # Read tag IDs from HuskyLens
    # ids is a LIST, e.g. []  or [1]  or  [3, 1]
    ids = camera.get_tag_ids()

    # -----------------------------
    # STUDENT TASK 2:
    # Complete the logic below.
    # Hint: use  "number in ids"  to check if a tag is in the list.
    #       Do NOT use ids == 2  (a list is never equal to a number).
    # -----------------------------

    if ______ in ids:
        # stop
        ______________________________
        display.show_________
        print(_________)
    elif ______ in ids:
        # move forward
        ______________________________
        display.show_________
        print(_________)
    elif ______ in ids:
        # turn (one motor slower)
        ______________________________
        display.show_________
        print(_________)
    else:
        # no tag - stop safely
        ______________________________
        display.show_________
        print(_________)

    # Delay 200 ms
    utime.sleep_ms(200)