class Joystick:
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
