#
# A virtual gamepad: shows a text-based (curses) to control the sticks and buttons of the default gamepad.
#
# To run this from the main project dir:
# PYTHONPATH=./src/python/ python3 examples/virtual_gamepad.py
#

from dbus.mainloop.glib import DBusGMainLoop
from bt_joystick import BTDevice, hid_report_descriptor
from bt_joystick.hid_report_descriptor import Usage
from virtual_device_ui import run

buttons = ['A', 'B', 'C', 'X', 'Y', 'Z', 'TL', 'TR', 'TL2', 'TR2', 'SELECT', 'START', 'MODE', 'THUMBL', 'THUMBR']
axes = [ 'X', 'Y', 'RX', 'RY' ]
sticks = [ ('X', 'Y'), ('RX', 'RY') ]

hid_descriptor = hid_report_descriptor.create_joystick_report_descriptor(kind=Usage.Gamepad, axes=(Usage.X, Usage.Y, Usage.Rx, Usage.Ry), hat_switch=True, button_number=15)

DBusGMainLoop(set_as_default=True)
device = BTDevice(hid_descriptor=hid_descriptor)
run('Virtual Gamepad', device, True, False, axes, sticks, buttons)
