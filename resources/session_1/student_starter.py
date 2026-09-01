import utime
from maqueen import Maqueen

# Session 1 student scaffold.
# TODO: complete the helper functions so the robot moves forward, waits, and stops.

robot = Maqueen()


def forward(speed=120):
    # TODO: use robot.set_motor() to drive both wheels forward.
    pass


def stop():
    # TODO: stop both motors using the verified Maqueen API.
    pass


def run_investigation():
    # TODO: test two different movement times and record what changed.
    forward(120)
    utime.sleep_ms(1000)
    stop()


while True:
    run_investigation()
    utime.sleep_ms(2000)
