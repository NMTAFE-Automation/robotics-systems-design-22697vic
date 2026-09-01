import utime
from maqueen import Maqueen

# Session 2 student scaffold.
# TODO: test movement speed, turning, and LED status indicators.

robot = Maqueen()


def drive(left_speed, right_speed, duration_ms):
    # TODO: set both motors, wait, then stop.
    pass


def show_status(left_on, right_on):
    # TODO: control the left and right LEDs.
    pass


def run_speed_test():
    for speed in (20, 50, 80, 100):
        # TODO: replace this placeholder with a real movement test.
        print("Test speed:", speed)
        utime.sleep_ms(500)


def run_turn_test():
    # TODO: create one left turn and one right turn.
    pass


while True:
    run_speed_test()
    run_turn_test()
    show_status(True, True)
    utime.sleep_ms(1000)
    show_status(False, False)
    utime.sleep_ms(2000)
