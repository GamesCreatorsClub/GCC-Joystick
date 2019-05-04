from approxeng.input import Controller, Button, CentredAxis, BinaryAxis

__all__ = ['GCCBTJoystick']


class GCCBTJoystick(Controller):
    """
    Driver for the GCC BT Joystick.
    """

    def __init__(self, dead_zone=0.05, hot_zone=0.05):
        """
        Create a new GCCBTJoystick driver

        :param float dead_zone:
            Used to set the dead zone for each :class:`approxeng.input.CentredAxis` in the controller.
        :param float hot_zone:
            Used to set the hot zone for each :class:`approxeng.input.CentredAxis` in the controller.
        """
        super(GCCBTJoystick, self).__init__(
            controls=[
                Button("D-pad Up", 304, sname='dup'),
                Button("D-pad Down", 305, sname='ddown'),
                Button("D-pad Left", 306, sname='dleft'),
                Button("D-pad Right", 307, sname='dright'),
                Button("Left Stick", 308, sname='ls'),
                Button("Right Stick", 309, sname='rs'),
                Button("Select", 310, sname='select'),
                Button("L1", 311, sname='l1'),
                Button("R1", 312, sname='r1'),
                Button("Start", 313, sname='start'),
                Button("Circle", 314, sname='circle'),
                Button("Cross", 315, sname='cross'),
                Button("Square", 316, sname='square'),
                Button("Triangle", 317, sname='triangle'),
                CentredAxis("Left Horizontal", -127, 127, 0, sname='lx'),
                CentredAxis("Left Vertical", -127, 127, 1, invert=True, sname='ly'),
                CentredAxis("Right Horizontal", -127, 255, 3, sname='rx'),
                CentredAxis("Right Vertical", -127, 127, 4, invert=True, sname='ry')
            ],
            dead_zone=dead_zone,
            hot_zone=hot_zone)

    @staticmethod
    def registration_ids():
        """
        :return: list of (vendor_id, product_id) for this controller
        """
        return [(0x1d6b, 0x246)]

    def __repr__(self):
        return 'GCC BT Joystick'
