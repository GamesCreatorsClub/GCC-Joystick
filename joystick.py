#
# Copyright 2019 Games Creators Club
#
# MIT License
#


class Joystick:

    def __init__(self):
        pass

    def readAxis(self):
        raise NotImplementedError()

    def readButtons(self):
        raise NotImplementedError()
