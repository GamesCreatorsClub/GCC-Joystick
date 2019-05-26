#
# Copyright 2019 Games Creators Club
#
# MIT License
#

class FakeJoystick:
    """
    A fake joystick implementation for testing: it just returns continuous axis movements and button presses.
    """
    def __init__(self):
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

    def readAxis(self):
        self.count = self.count + self.direction
        if self.count > 127:
            self.count = 0
            self.direction = -1
        elif self.count < -127:
            self.count = 0
            self.direction = 1
        return { 'x': self.count + 127, 'y': self.count + 127, 'rx': self.count + 127, 'ry': self.count + 127 }

    def readButtons(self):
        for b in self.buttons:
            self.buttons[b] = not self.buttons[b]
        return self.buttons


if __name__ == "__main__":

    import sys, os
    sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

    from bluetooth_joystick import BluetoothJoystick

    bluetooth_joystick = BluetoothJoystick(FakeJoystick())
    bluetooth_joystick.run()
