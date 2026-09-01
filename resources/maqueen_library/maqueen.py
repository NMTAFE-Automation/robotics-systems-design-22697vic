"""
Updated By: John Robertson (GitHub: Robbo-lab)
Initial code taken and adapted from: Python class for DFRobot Micro:maqueen platform
https://www.dfrobot.com/product-1783.html
Author: Krzysztof Sawicki <krzysztof@rssi.pl>
License: GNU
"""
import microbit
import machine
import utime
import neopixel

class Maqueen:
    """
        Initial code taken and adapted from: Python class for DFRobot Micro:maqueen platform
        https://www.dfrobot.com/product-1783.html
        Author: Krzysztof Sawicki <krzysztof@rssi.pl>
        License: GNU

        This class provides an interface to control the Maqueen robot using MicroPython.
        It includes methods for controlling motors, LEDs, NeoPixel RGB lights, line sensors,
        ultrasonic distance measurement, and servos.

        Attributes:
            neo (NeoPixel): A NeoPixel instance for controlling RGB lights.
    """

    def __init__(self):
        """
        Initialises the Maqueen robot by setting up the NeoPixel LEDs and ensuring
        the distance sensor is ready.
        """
        self.neo = neopixel.NeoPixel(microbit.pin15, 4)
        # self.rgbleds = neopixel.NeoPixel(microbit.pin15, 4)
        microbit.pin1.write_digital(0)
        print("Robot initialised")


    # value: {0,1}
    def led_left(self, value):
        """
        Controls the left LED.
        param: value (int): 1 to turn ON, 0 to turn OFF.
        Example:
            >>> robot.led_left(1)  # Turns ON left LED
            >>> utime.sleep(1)
            >>> robot.led_left(0)  # Turns OFF left LED
        """
        microbit.pin8.write_digital(value)


    # value: {0,1}
    def led_right(self, value):
        """
        Controls the right LED.
        param: value (int): 1 to turn ON, 0 to turn OFF.
        Example:
            >>> robot.led_right(1)  # Turns ON right LED
            >>> utime.sleep(1)
            >>> robot.led_right(0)  # Turns OFF right LED
        """
        microbit.pin12.write_digital(value)


    def rgb_front_left(self, red, green, blue):
        """
        Sets the color of the front left RGB LED.
        param: red (int): Red component (0-255).
        param: green (int): Green component (0-255).
        param: blue (int): Blue component (0-255).
        Example:
            >>> robot.rgb_front_left(255, 0, 0)  # Sets red color
            >>> utime.sleep(1)
            >>> robot.rgb_front_left(0, 0, 0)  # Turns off LED
        """
        self.neo[0] = (red, green, blue)
        self.neo.show()


    def rgb_rear_left(self, red, green, blue):
        """
        Sets the color of the rear left RGB LED.
        """
        self.neo[1] = (red, green, blue)
        self.neo.show()


    def rgb_rear_right(self, red, green, blue):
        """
        Sets the color of the rear right RGB LED.
        """
        self.neo[2] = (red, green, blue)
        self.neo.show()


    def rgb_front_right(self, red, green, blue):
        """
        Sets the color of the front right RGB LED.
        """
        self.neo[3] = (red, green, blue)
        self.neo.show()


    def read_distance(self):
        """
        Reads distance from HC SR04 ultrasonic sensor
        The result is in centimeters
        Returns: float: The distance in centimeters.
        Example:
            >>> distance = robot.read_distance()
            >>> print("Measured Distance:", distance, "cm")
        """
        divider = 42
        maxtime = 250 * divider

        microbit.pin2.read_digital()  # just for setting PULL_DOWN on pin2
        microbit.pin1.write_digital(0)
        utime.sleep_us(2)
        microbit.pin1.write_digital(1)
        utime.sleep_us(10)
        microbit.pin1.write_digital(0)

        duration = machine.time_pulse_us(microbit.pin2, 1, maxtime)
        distance = duration / divider

        return distance


    def ultrasound_measure(self):
        """
        Measures distance using the ultrasonic sensor.
        Returns: int: Distance in cm, -1 if timeout, -2 if echo is too long.
        """
        microbit.pin1.write_digital(1)
        utime.sleep_us(10)
        microbit.pin1.write_digital(0)

        # Wait for echo pin to become high
        timeout = utime.ticks_us()
        while True:
            pulseBegin = utime.ticks_us()
            if 1 == microbit.pin2.read_digital():
                break
            if (pulseBegin - timeout) > 5000:
                return -1

        # Measure time until echo pin becomes low
        while True:
            pulseEnd = utime.ticks_us()
            if 0 == microbit.pin2.read_digital():
                break
            if (pulseEnd - pulseBegin) > 5000:
                return -2

            # Time = Width of Echo pulse in us
            pulse_time = pulseEnd - pulseBegin

            # Distance in cm = Time / 58
            distance = pulse_time / 58
            return int(distance)


    def set_motor(self, motor, value):
        """
        Controls the motor.
        param: motor (int): 0 for left motor, 1 for right motor.
        param: value (int): Speed (-255 to 255), sign determines direction.
        Example:
            >>> robot.set_motor(0, 100)  # Left motor forward at speed 100
            >>> utime.sleep(2)
            >>> robot.set_motor(1, -100)  # Right motor reverse at speed 100
        """
        # Exit early if not a motor
        if motor not in (0, 1):
            raise ValueError("motor must be 0 (left) or 1 (right)")
        
        # Ensure value does not exceed -255 to 255
        value = max(-255, min(value, 255))

        data = bytearray(3)

        # Motor selection: 0 for left, 2 for right
        data[0] = 0 if motor == 0 else 2

        # Set direction (1 = reverse, 0 = forward)
        if value < 0:
            data[1] = 1
            value = -value  # Convert to positive
        else:
            data[1] = 0

        # Ensure speed is within range 0-255
        data[2] = min(value, 255)

        # Send command to I2C motor driver
        microbit.i2c.write(0x10, data)


    def motor_stop_all(self):
        """
        Stops both motors.
        Example:
            >>> robot.motor_stop_all()  # Stops all movement
        """
        self.set_motor(0, 0)
        self.set_motor(1, 0)


    def read_patrol(self, sensor):
        """
        Reads the line-following sensor.
        param: which (int): 0 for left sensor, 1 for right sensor.
        Returns: int: 1 if detecting a line, 0 otherwise.
        Example:
            >>> left_line = robot.read_patrol(0)
            >>> right_line = robot.read_patrol(1)
            >>> if left_line:
            >>>     print("Left sensor detected a line")
        """
        if sensor == 0:  # left
            return microbit.pin13.read_digital()
        elif sensor == 1:  # right
            return microbit.pin14.read_digital()
        
        raise ValueError("sensor must be 0 (left) or 1 (right)")


    # return: {0,1}
    def line_left(self):
        """
        Reads the left line-following sensor.
        Returns:int: 1 if detecting a line, 0 otherwise.
        """
        return microbit.pin13.read_digital()


    # return: {0,1}
    def line_right(self):
        """
        Reads the right line-following sensor.
        Returns: int: 1 if detecting a line, 0 otherwise.
        """
        return microbit.pin14.read_digital()


    def follow_line(self, speed=80):
        """
        Performs one step of line-following logic using the left and right sensors.

        The robot will:
        - Stop if both sensors detect a line
        - Turn left if only the left sensor detects a line
        - Turn right if only the right sensor detects a line
        - Move forward if no line is detected

        Example:
            >>> robot.follow_line()
            >>> utime.sleep(0.1)
        """
        left = self.line_left()
        right = self.line_right()

        if left and right:
            self.motor_stop_all()
        elif left:
            # Turn left → stop left motor, run right motor
            self.set_motor(0, 0)
            self.set_motor(1, speed)
        elif right:
            # Turn right → run left motor, stop right motor
            self.set_motor(0, speed)
            self.set_motor(1, 0)
        else:
            # Move forward
            self.set_motor(0, speed)
            self.set_motor(1, speed)


    def stop_if_close(self, threshold=10):
        """
        Stops the robot if an object is detected within a specified distance.

        This function reads the ultrasonic sensor and compares the measured
        distance to the threshold value.

        Example:
            >>> if robot.stop_if_close(15):
            >>>     print("Object detected - stopping")
        """
        distance = self.read_distance()

        if distance > 0 and distance < threshold:
            self.motor_stop_all()
            return True

        return False