#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#

import os
import sys
import RPi.GPIO as GPIO
import time

from smbus import SMBus
from bt_joystick import Joystick, BluetoothJoystickDeviceMain


class ExplorerPHatJoystick(Joystick):
    # Based on https://github.com/pimoroni/explorer-hat/blob/master/library/explorerhat/ads1015.py

    UP = 18
    DOWN = 27
    LEFT = 0
    RIGHT = 17

    LB = 1
    RB = 5

    TRIGGER = 25
    TR = 23
    TL = 24
    THUMB = 22

    PGA_6_144V = 6144
    PGA_4_096V = 4096
    PGA_2_048V = 2048
    PGA_1_024V = 1024
    PGA_0_512V = 512
    PGA_0_256V = 256

    REG_CONV = 0x00
    REG_CFG = 0x01

    def __init__(self):
        self.address = 0x48
        self.i2c = SMBus(1)

        self.samples_per_second_map = {128: 0x0000, 250: 0x0020, 490: 0x0040, 920: 0x0060, 1600: 0x0080, 2400: 0x00A0, 3300: 0x00C0}
        self.channel_map = {0: 0x4000, 1: 0x5000, 2: 0x6000, 3: 0x7000}
        self.programmable_gain_map = {6144: 0x0000, 4096: 0x0200, 2048: 0x0400, 1024: 0x0600, 512: 0x0800, 256: 0x0A00}

        self.axes = {Joystick.X: 0.0, Joystick.Y: 0.0, Joystick.Rx: 0.0, Joystick.Ry: 0.0}
        self.buttons = {'trigger': False, 'tl': False, 'tr': False, 'thumb': False, 'dpad_up': False, 'dpad_down': False, 'dpad_left': False, 'dpad_right': False, 'thumbl': False, 'thumbr': False}

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(ExplorerPHatJoystick.UP, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.DOWN, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.LEFT, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.RIGHT, GPIO.IN)

        GPIO.setup(ExplorerPHatJoystick.LB, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.RB, GPIO.IN)

        GPIO.setup(ExplorerPHatJoystick.TRIGGER, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.TR, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.TL, GPIO.IN)
        GPIO.setup(ExplorerPHatJoystick.THUMB, GPIO.IN)

    def _read_se_adc(self, channel=1, programmable_gain=6144, samples_per_second=1600):
        # sane defaults
        config = 0x0003 | 0x0100

        config |= self.samples_per_second_map[samples_per_second]
        config |= self.channel_map[channel]
        config |= self.programmable_gain_map[programmable_gain]

        # set "single shot" mode
        config |= 0x8000

        # write single conversion flag
        self.i2c.write_i2c_block_data(self.address, ExplorerPHatJoystick.REG_CFG, [(config >> 8) & 0xFF, config & 0xFF])

        delay = (1.0 / samples_per_second) + 0.0001
        time.sleep(delay)

        data = self.i2c.read_i2c_block_data(self.address, ExplorerPHatJoystick.REG_CONV)

        return (((data[0] << 8) | data[1]) >> 4) * programmable_gain / 2048.0 / 1000.0

    @staticmethod
    def _fix(v):
        r = int(((v - 2.5) / 2.5) * 127)
        if r < 0:
            r = 256 + r
        elif r > 127:
            r = 127

        try:
            c = chr(r)
        except Exception as e:
            print("Failed to convert " + str(v) + " got " + str(r))
            r = 0

        # print("Read joystick value as " + str(v) + " fixed it to " + str(r))
        return r

    @property
    def defined_button_number(self):
        return 14

    @property
    def defined_axes(self):
        return [Joystick.X, Joystick.Y, Joystick.Rx, Joystick.Ry]

    def read_axes(self):
        self.axes[Joystick.Rx] = self._fix(self._read_se_adc(3))
        self.axes[Joystick.Ry] = self._fix(self._read_se_adc(0))
        self.axes[Joystick.X] = self._fix(self._read_se_adc(2))
        self.axes[Joystick.Y] = self._fix(self._read_se_adc(1))
        return self.axes

    def read_buttons(self):
        old_bind = self.buttons['dpad_up']

        self.buttons['dpad_up'] = not bool(GPIO.input(ExplorerPHatJoystick.UP))
        self.buttons['dpad_down'] = not bool(GPIO.input(ExplorerPHatJoystick.DOWN))
        self.buttons['dpad_left'] = not bool(GPIO.input(ExplorerPHatJoystick.LEFT))
        self.buttons['dpad_right'] = not bool(GPIO.input(ExplorerPHatJoystick.RIGHT))

        self.buttons['thumbl'] = not bool(GPIO.input(ExplorerPHatJoystick.LB))
        self.buttons['thumbr'] = not bool(GPIO.input(ExplorerPHatJoystick.RB))

        self.buttons['trigger'] = not bool(GPIO.input(ExplorerPHatJoystick.TRIGGER))
        self.buttons['tl'] = not bool(GPIO.input(ExplorerPHatJoystick.TL))
        self.buttons['tr'] = not bool(GPIO.input(ExplorerPHatJoystick.TR))
        self.buttons['thumb'] = not bool(GPIO.input(ExplorerPHatJoystick.THUMB))

        new_bind = self.buttons['dpad_up']
        if not old_bind and new_bind:
            print("Got change on dpad_up - setting to pairable")
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
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")

    from bt_joystick import BluetoothJoystickDeviceMain

    bluetooth_joystick = BluetoothJoystickDeviceMain(ExplorerPHatJoystick())
    bluetooth_joystick.run()
