# Runs on the Maqueen robot's micro:bit to receive movement commands from the Raspberry Pi.
from microbit import *
from maqueen import Maqueen

robot = Maqueen()
uart.init(baudrate=115200)
display.show("R")

while True:
    if uart.any():
        cmd = uart.readline().strip()

        if cmd == b'f':
            display.show("F")
            robot.set_motor(0, 120)
            robot.set_motor(1, 120)
        elif cmd == b'b':
            display.show("B")
            robot.set_motor(0, -120)
            robot.set_motor(1, -120)
        elif cmd == b'l':
            display.show("L")
            robot.set_motor(0, 0)
            robot.set_motor(1, 120)
        elif cmd == b'r':
            display.show("R")
            robot.set_motor(0, 120)
            robot.set_motor(1, 0)
        elif cmd == b's':
            display.show("S")
            robot.motor_stop_all()
