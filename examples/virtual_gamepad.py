#
# A virtual gamepad: shows a text-based (curses) to control the sticks and buttons of the default gamepad.
#
# To run this from the main project dir:
# PYTHONPATH=./src/python/ python3 examples/virtual_gamepad.py
#

from dbus.mainloop.glib import DBusGMainLoop
from bt_joystick import BTDevice
from virtual_device_ui import run

buttons = ['A', 'B', 'C', 'X', 'Y', 'Z', 'TL', 'TR', 'TL2', 'TR2', 'SELECT', 'START', 'MODE', 'THUMBL', 'THUMBR']
axes = [ 'X', 'Y', 'RX', 'RY' ]
sticks = [ ('X', 'Y'), ('RX', 'RY') ]

DBusGMainLoop(set_as_default=True)
device = BTDevice()
run(device, False, axes, sticks, buttons)
