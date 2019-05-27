#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#


import time

from dbus.mainloop.glib import DBusGMainLoop
from bt_joystick import BTDevice

from bt_joystick.hid_report_descriptor import create_joystick_report_descriptor, Usage


class Joystick:

    X = Usage.X
    Y = Usage.Y
    Z = Usage.Z
    Rx = Usage.Rx
    Ry = Usage.Ry
    Rz = Usage.Rz
    Slider = Usage.Slider
    Dial = Usage.Dial
    Wheel = Usage.Wheel

    def __init__(self):
        pass

    @property
    def defined_kind(self):
        return Usage.Gamepad

    @property
    def defined_button_number(self):
        raise NotImplementedError("Please return number of buttons your joystick implements")

    @property
    def defined_axes(self):
        raise NotImplementedError("Please return defined axes your joystick implements")

    def read_axis(self):
        raise NotImplementedError("Please return an dictionary with defined axes values")

    def read_buttons(self):
        raise NotImplementedError("Please return array of 1/0 or 'True'/'False' values for defined buttons")


class BluetoothJoystickDeviceMain:
    def __init__(self, joystick, reading_frequency=10):
        self.joystick = joystick
        self.reading_frequency = reading_frequency

        self.button_number = joystick.defined_button_number
        self.axes = joystick.defined_axes

        self.only_changes = True
        self.do_run = True

        self.button_bits = [0] * ((self.button_number - 1) // 8 + 1)
        self.new_button_bits = [0] * len(self.button_bits)

        self.axes_data = [0] * len(self.axes)
        self.new_axes_data = [0] * len(self.axes)

        self.hid_descriptor = None
        self.bt = None

    def init(self):
        self.hid_descriptor = create_joystick_report_descriptor(
            kind=self.joystick.defined_kind,
            axes=self.axes,
            button_number=self.button_number
        )

        self.bt = BTDevice(hid_descriptor=self.hid_descriptor)

    def read_joystick_values(self):
        joystick_axes = self.joystick.read_axes()
        joystick_buttons = self.joystick.read_buttons()

        i = 0
        for axis in self.axes:
            self.new_axes_data[i] = joystick_axes[axis]
            i += 1

        i = 0
        bit = 1
        for button_state in joystick_buttons:
            if button_state:
                self.new_button_bits[i] |= bit
            else:
                self.new_button_bits[i] &= ~bit

            bit *= 2
            if bit == 256:
                bit = 1
                i += 1

    def has_joystick_changes(self):
        has_changes = False

        for i in range(0, len(self.axes_data)):
            if self.axes_data[i] != self.new_axes_data[i]:
                self.axes_data[i] = self.new_axes_data[i]
                has_changes = True

        for i in range(0, len(self.new_button_bits)):
            if self.button_bits[i] != self.new_button_bits[i]:
                self.button_bits[i] = self.new_button_bits[i]
                has_changes = True

        return has_changes

    def send_joystick_values(self):
        data = bytes((0xA1, 0x01)) + bytes(self.button_bits) + bytes(self.new_axes_data)

        # print("Changing data " + str(["{:02x}".format(d) for d in data]))
        try:
            self.bt.send_message(data)
            return True
        except Exception as e:
            print("Failed to send data - disconnected " + str(e))
            return False

    def loop(self):
        while self.do_run:
            time.sleep(1 / self.reading_frequency)

            self.read_joystick_values()

            if not self.only_changes or self.has_joystick_changes():
                successful = self.send_joystick_values()
                if not successful:
                    return

    def run(self):
        DBusGMainLoop(set_as_default=True)

        self.init()

        while self.do_run:
            print("Waiting for connections")
            self.bt.listen()

            self.loop()
