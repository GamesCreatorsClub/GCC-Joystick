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

    @property
    def defined_button_number(self):
        return 10

    @property
    def defined_axes(self):
        return [Joystick.X, Joystick.Y, Joystick.Rx, Joystick.Ry]

    def read_axes(self):
        self.count = self.count + self.direction
        if self.count > 127:
            self.count = 0
            self.direction = -1
        elif self.count < -127:
            self.count = 0
            self.direction = 1
        return { Joystick.X: self.count + 127, Joystick.Y: self.count + 127, Joystick.Rx: self.count + 127, Joystick.Ry: self.count + 127 }

    def read_buttons(self):
        for b in self.buttons:
            self.buttons[b] = not self.buttons[b]
        self.start_pairing()
        return [
            self.buttons['trigger'],
            self.buttons['thumbl'],
            self.buttons['thumbr'],
            self.buttons['thumb'],
            self.buttons['tl'],
            self.buttons['tr'],
            self.buttons['dpad_up'],
            self.buttons['dpad_down'],
            self.buttons['dpad_left'],
            self.buttons['dpad_right']]


if __name__ == "__main__":

    import sys, os
    sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])

    bluetooth_joystick = BluetoothJoystickDeviceMain(FakeJoystick())
    bluetooth_joystick.run()
