from microbit import display
import utime
from maqueen import Maqueen
from huskyadapter import HuskyAdapter

# Session 7 lecturer reference solution using the verified HuskyLens API.
# Tracks AprilTag blocks and reacts to centroid movement.

robot = Maqueen()
camera = HuskyAdapter()


def drive(left_speed, right_speed):
    robot.set_motor(0, left_speed)
    robot.set_motor(1, right_speed)


while True:
    result = camera.get_result()
    blocks = result["blocks"]

    if not blocks:
        display.show("?")
        robot.motor_stop_all()
        utime.sleep_ms(150)
        continue

    block = blocks[0]
    cx = block.x
    cy = block.y
    print("ID=%d x=%d y=%d w=%d h=%d" % (block.ID, block.x, block.y, block.w, block.h))

    if cx < 130:
        display.show("L")
        drive(-80, 80)
    elif cx > 190:
        display.show("R")
        drive(80, -80)
    else:
        display.show("F")
        drive(100, 100)

    # Expected observation: larger bounding boxes usually mean a closer tag.
    if block.w > 90:
        display.show("S")
        robot.motor_stop_all()

    utime.sleep_ms(150)