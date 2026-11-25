# -----------------------------
# Assessment Task 3 – Tag Follower (STUDENT START CODE)
# HuskyLens (Tag Recognition) -> Maqueen robot
#
# AT2 only used the tag ID.  AT3 also uses WHERE the tag is
# and HOW BIG it is in the camera picture.
#
# Tag 2           -> stop (always wins)
# Tag 1 on left   -> turn left
# Tag 1 on right  -> turn right
# Tag 1 centre    -> move forward
# Tag 1 very big  -> stop (robot is close enough)
# No tag          -> stop safely
#
# HuskyLens picture is 320 wide x 240 high.
# x = centre of the tag, 0 (left) ... 160 (middle) ... 320 (right)
# w = width of the tag in pixels (bigger = closer)
#
# Rename this file to main.py before flashing.
# Fill in every ______ line.
# -----------------------------
from maqueen import Maqueen
from huskyadapter import HuskyAdapter
from microbit import display
import utime

robot = Maqueen()
camera = HuskyAdapter()          # Tag Recognition is the default

SPEED = 80                       # normal motor speed
SLOW = 30                        # slower motor when turning
LEFT_LIMIT = 120                 # x smaller than this = tag is on the left
RIGHT_LIMIT = 200                # x bigger than this  = tag is on the right
CLOSE_WIDTH = 90                 # w bigger than this  = close enough, stop


def read_blocks(attempts=3):
    # Read blocks from HuskyLens. Retry if the read is empty,
    # because the camera sometimes misses a frame.
    for _ in range(attempts):
        blocks = camera.get_result()["blocks"]
        if blocks:
            return blocks
        utime.sleep_ms(30)
    return []


def find_tag(blocks, tag_id):
    # Returns the block with this tag ID, or None if not seen
    for block in blocks:
        if block.ID == tag_id:
            return block
    return None


# -----------------------------
# STUDENT TASK 1:
# Complete the four movement functions.
# Hint: robot.set_motor(0, speed) = left motor
#       robot.set_motor(1, speed) = right motor
#       To turn LEFT, the LEFT motor must be slower.
# -----------------------------
def forward():
    ______________________________
    ______________________________


def turn_left():
    ______________________________
    ______________________________


def turn_right():
    ______________________________
    ______________________________


def stop():
    ______________________________


while True:
    # Read all blocks (tags) from HuskyLens in ONE read
    blocks = read_blocks()
    stop_tag = find_tag(blocks, 2)
    target = find_tag(blocks, 1)

    # -----------------------------
    # STUDENT TASK 2:
    # Complete the logic below.
    # Hint: target.x is the tag position, target.w is the tag width.
    #       Check "is not None" before using target.x or target.w
    # -----------------------------

    if stop_tag is not None:
        # tag 2 seen - stop
        ______________________________
        display.show_________
        print(_________)
    elif target is None:
        # no tag 1 - stop safely
        ______________________________
        display.show_________
        print(_________)
    elif target.______ > CLOSE_WIDTH:
        # tag 1 is close - stop
        ______________________________
        display.show_________
        print(_________)
    elif target.______ < LEFT_LIMIT:
        # tag 1 on the left
        ______________________________
        display.show_________
        print(_________)
    elif target.______ > RIGHT_LIMIT:
        # tag 1 on the right
        ______________________________
        display.show_________
        print(_________)
    else:
        # tag 1 in the middle - go forward
        ______________________________
        display.show_________
        print(_________)

    # -----------------------------
    # STUDENT TASK 3:
    # Test and tune SPEED, SLOW, LEFT_LIMIT, RIGHT_LIMIT and CLOSE_WIDTH.
    # Write down the values that worked best and why.
    # -----------------------------

    # Delay 100 ms
    utime.sleep_ms(100)
