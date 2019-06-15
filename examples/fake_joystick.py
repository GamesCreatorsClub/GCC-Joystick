#
# Copyright 2019 Games Creators Club
#
# MIT License
#

from bt_joystick import Joystick, BluetoothJoystickDeviceMain

class FakeJoystick(Joystick):
    """
    A fake joystick implementation for testing: it just returns continuous axis movements and button presses.
    """
    def __init__(self):
        super(FakeJoystick, self).__init__()
        self.count = 0
        self.direction = 1
        self.buttons = {
            'dpad_up': False,
            'dpad_down': False,
            'dpad_left': False,
            'dpad_right': False,
            'thumbl': False,
            'thumbr': False,
            'trigger': False,
            'tl': False,
            'tr': False,
            'thumb': False,
        }

    def read_axes(self):
        self.count = self.count + self.direction
        if self.count > 127:
            self.count = 0
            self.direction = -1
        elif self.count < -127:
            self.count = 0
            self.direction = 1
        return { 'x': self.count + 127, 'y': self.count + 127, 'rx': self.count + 127, 'ry': self.count + 127 }

    def read_buttons(self):
        for b in self.buttons:
            self.buttons[b] = not self.buttons[b]
        return self.buttons


if __name__ == "__main__":

    import sys, os
    sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

    bluetooth_joystick = BluetoothJoystickDeviceMain(FakeJoystick())
    bluetooth_joystick.run()
