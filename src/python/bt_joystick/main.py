#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#


import time

from dbus.mainloop.glib import DBusGMainLoop
from bt_joystick import BTDevice

# if not os.geteuid() == 0:
#     sys.exit("Only root can run this script")


class Joystick:

    def __init__(self):
        pass

    def readAxis(self):
        raise NotImplementedError()

    def readButtons(self):
        raise NotImplementedError()

    # TODO Add way for Joystick implementation to pass 'description' to Main class
    # so it can create appropriate SDP record and handle results


class BluetoothJoystickDeviceMain:
    def __init__(self, joystick):
        self.joystick = joystick

    def run(self):
        DBusGMainLoop(set_as_default=True)

        bt = BTDevice()

        while True:
            re_start = False

            print("Waiting for connections")
            bt.listen()

            button_bits_1 = 0
            button_bits_2 = 0

            axis = [0, 0, 0, 0]
            new_axis = [0, 0, 0, 0]

            while not re_start:
                time.sleep(0.1)

                joystick_axis = self.joystick.readAxis()
                joystick_buttons = self.joystick.readButtons()

                new_axis[0] = joystick_axis['x']
                new_axis[1] = joystick_axis['y']
                new_axis[2] = joystick_axis['rx']
                new_axis[3] = joystick_axis['ry']

                new_button_bits_1 = 0
                new_button_bits_2 = 0

                # TODO this should really use Joystick description to determine which buttons are sent as which
                # 'trigger', 'tl', 'tr', 'thumb', 'dpad_up', 'dpad_down', 'dpad_left', 'dpad_right', 'thumbl', 'thumbr'
                if joystick_buttons['dpad_up']:
                    new_button_bits_1 |= 1
                if joystick_buttons['dpad_down']:
                    new_button_bits_1 |= 2
                if joystick_buttons['dpad_left']:
                    new_button_bits_1 |= 4
                if joystick_buttons['dpad_right']:
                    new_button_bits_1 |= 8

                if joystick_buttons['trigger']:
                    new_button_bits_1 |= 16
                if joystick_buttons['tl']:
                    new_button_bits_1 |= 32
                if joystick_buttons['tr']:
                    new_button_bits_1 |= 64
                if joystick_buttons['thumb']:
                    new_button_bits_1 |= 128

                if joystick_buttons['thumbl']:
                    new_button_bits_2 |= 1
                if joystick_buttons['thumbr']:
                    new_button_bits_2 |= 2

                has_changes = False

                for i in range(0, 4):
                    if axis[i] != new_axis[i]:
                        axis[i] = new_axis[i]
                        has_changes = True

                if button_bits_1 != new_button_bits_1 or button_bits_2 != new_button_bits_2:
                    button_bits_1 = new_button_bits_1
                    button_bits_2 = new_button_bits_2
                    has_changes = True

                if has_changes:
                    data = bytes((0xA1, 0x01, button_bits_1, button_bits_2, axis[0], axis[1], axis[2], axis[3]))

                    # print("Changing data " + str(["{:02x}".format(d) for d in data]))
                    try:
                        bt.send_message(data)
                    except Exception as e:
                        print("Failed to send data - disconnected " + str(e))
                        re_start = True
