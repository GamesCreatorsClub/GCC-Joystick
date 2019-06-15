#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#
import threading
import time
import sys

from dbus.mainloop.glib import DBusGMainLoop
from bt_joystick import BTDevice

from bt_joystick.hid_report_descriptor import create_joystick_report_descriptor, Usage
from gi.repository import GObject


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
        self.bd_device = None

    def _set_bluetooth_device(self, bt_device):
        self.bt_device = bt_device

    def start_pairing(self):
        self.bt_device.allow_pairing(True)
        self.bt_device.set_discoverable(True)

    @property
    def defined_kind(self):
        return Usage.Gamepad

    @property
    def defined_button_number(self):
        raise NotImplementedError("Please return number of buttons your joystick implements")

    @property
    def defined_axes(self):
        raise NotImplementedError("Please return defined axes your joystick implements")

    def read_axes(self):
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
        self._do_run = True
        self._gobject_loop_exception = None

        self.button_bits = [0] * ((self.button_number - 1) // 8 + 1)
        self.new_button_bits = [0] * len(self.button_bits)

        self.axes_data = [0] * len(self.axes)
        self.new_axes_data = [0] * len(self.axes)

        self.hid_descriptor = None
        self.bt_device = None

        self.connected = False

    def init(self):
        DBusGMainLoop(set_as_default=True)

        self.hid_descriptor = create_joystick_report_descriptor(
            kind=self.joystick.defined_kind,
            axes=self.axes,
            button_number=self.button_number
        )

        self.bt_device = BTDevice(hid_descriptor=self.hid_descriptor)
        self.bt_device.set_discoverable(False)  # Ensure that on start up we are not discoverable
        self.joystick._set_bluetooth_device(self.bt_device)

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
            self.bt_device.send_message(data)
            return True
        except Exception as e:
            print("Failed to send data - disconnected; " + str(e))
            return False

    def setup_gobject_mainloop(self):
        def main_loop():
            try:
                print("Staring GTK main loop...")
                mainloop.run()
                print("Stopped GTK main loop.")
            except KeyboardInterrupt as e:
                print("Got keyboard exception in thread; " + str(e))
                mainloop.quit()
                self._gobject_loop_exception = e
            except Exception as e:
                print("Got exception in thread; " + str(e))
                mainloop.quit()
                self._gobject_loop_exception = e

        mainloop = GObject.MainLoop()

        thread = threading.Thread(target=main_loop)
        thread.setDaemon(True)
        thread.start()

    def loop(self):
        if self._gobject_loop_exception is not None:
            raise self._gobject_loop_exception

        if not self.connected:
            self.connected = self.bt_device.listen(1 / self.reading_frequency)
            if self.connected:
                self.bt_device.allow_pairing(False)
                self.bt_device.set_discoverable(False)
        else:
            time.sleep(1 / self.reading_frequency)

        self.read_joystick_values()

        if self.connected and (not self.only_changes or self.has_joystick_changes()):
            successful = self.send_joystick_values()
            if not successful:
                print("Failed to send values - disconnecting")
                # TODO add proper disconnect 'try' here...
                self.connected = False

    def run(self):
        self.init()
        self.setup_gobject_mainloop()

        while self._do_run:
            self.loop()
