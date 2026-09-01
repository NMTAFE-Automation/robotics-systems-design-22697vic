from microbit import *
from maqueen import Maqueen
# used for delays
import utime
import music
# When ready to attach the huskylens uncomment this line
# from huskyadapter import HuskyAdapter

# Initialise Maqueen
robot = Maqueen()
print("Starting Maqueen test...")

# Play the finished melody
music.play(music.POWER_UP)

print("All tests completed!")