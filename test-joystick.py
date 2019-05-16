#
# Copyright 2019 Games Creators Club
#
# MIT License
#

import time
from fake_joystick import Joystick

joystick = Joystick()

while True:
    time.sleep(0.5)

    axis = joystick.readAxis()
    buttons = joystick.readButtons()

    axis_string = " ".join([f + ": {: 5.2f}".format(axis[f]) for f in ['x', 'y', 'rx', 'ry']])
    buttons_string = " ".join([b + ":" + ('1' if buttons[b] else '0') for b in buttons])

    print(axis_string + " " + buttons_string)
