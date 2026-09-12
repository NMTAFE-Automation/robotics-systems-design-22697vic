import machine
import microbit
import neopixel
import utime


class Maqueen:
    def __init__(self):
        self.neo = neopixel.NeoPixel(microbit.pin15, 4)
        microbit.pin1.write_digital(0)
        print("Robot initialised")

    def led_left(self, value):
        microbit.pin8.write_digital(value)

    def led_right(self, value):
        microbit.pin12.write_digital(value)

    def _rgb(self, index, red, green, blue):
        self.neo[index] = (red, green, blue)
        self.neo.show()

    def rgb_front_left(self, red, green, blue):
        self._rgb(0, red, green, blue)

    def rgb_rear_left(self, red, green, blue):
        self._rgb(1, red, green, blue)

    def rgb_rear_right(self, red, green, blue):
        self._rgb(2, red, green, blue)

    def rgb_front_right(self, red, green, blue):
        self._rgb(3, red, green, blue)

    def read_distance(self):
        divider = 42
        maxtime = 250 * divider
        microbit.pin2.read_digital()
        microbit.pin1.write_digital(0)
        utime.sleep_us(2)
        microbit.pin1.write_digital(1)
        utime.sleep_us(10)
        microbit.pin1.write_digital(0)
        return machine.time_pulse_us(microbit.pin2, 1, maxtime) / divider

    def ultrasound_measure(self):
        microbit.pin1.write_digital(1)
        utime.sleep_us(10)
        microbit.pin1.write_digital(0)
        timeout = utime.ticks_us()
        while True:
            pulse_begin = utime.ticks_us()
            if microbit.pin2.read_digital() == 1:
                break
            if pulse_begin - timeout > 5000:
                return -1
        while True:
            pulse_end = utime.ticks_us()
            if microbit.pin2.read_digital() == 0:
                break
            if pulse_end - pulse_begin > 5000:
                return -2
            return int((pulse_end - pulse_begin) / 58)

    def set_motor(self, motor, value):
        if motor not in (0, 1):
            raise ValueError("motor must be 0 (left) or 1 (right)")
        value = max(-255, min(value, 255))
        data = bytearray(3)
        data[0] = 0 if motor == 0 else 2
        if value < 0:
            data[1] = 1
            value = -value
        else:
            data[1] = 0
        data[2] = value
        microbit.i2c.write(0x10, data)

    def motor_stop_all(self):
        self.set_motor(0, 0)
        self.set_motor(1, 0)

    def read_patrol(self, sensor):
        if sensor == 0:
            return microbit.pin13.read_digital()
        if sensor == 1:
            return microbit.pin14.read_digital()
        raise ValueError("sensor must be 0 (left) or 1 (right)")

    def line_left(self):
        return microbit.pin13.read_digital()

    def line_right(self):
        return microbit.pin14.read_digital()

    def follow_line(self, speed=80):
        left = self.line_left()
        right = self.line_right()
        if left and right:
            self.motor_stop_all()
        elif left:
            self.set_motor(0, 0)
            self.set_motor(1, speed)
        elif right:
            self.set_motor(0, speed)
            self.set_motor(1, 0)
        else:
            self.set_motor(0, speed)
            self.set_motor(1, speed)

    def stop_if_close(self, threshold=10):
        distance = self.read_distance()
        if 0 < distance < threshold:
            self.motor_stop_all()
            return True
        return False
