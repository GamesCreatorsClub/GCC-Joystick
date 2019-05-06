#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#

# Based on https://github.com/yaptb/BlogCode

import os
import sys
import time
import socket

import sdp_record
import hid_report_descriptor

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from joystick import Joystick

from bt_device_classes import LIMITED_DISCOVERABLE_MODE, PERIPHERAL, GAMEPAD


class BTDevice(dbus.service.Object):
    P_CTRL = 17  # Service port - must match port configured in SDP record
    P_INTR = 19  # Service port - must match port configured in SDP record#Interrrupt port
    PROFILE_DBUS_PATH = "/bluez/gcc/gcc_joy_profile"  # dbus path of  the bluez profile we will create

    def __init__(self, device_name='gcc-bt-joystick',
                 device_class=LIMITED_DISCOVERABLE_MODE | PERIPHERAL | GAMEPAD,
                 uuid="00001124-0000-1000-8000-00805f9b34fb",
                 service_name='org.gcc.btservice'):

        self.device_name = device_name
        self.device_class = device_class
        self.uuid = uuid
        self.service_name = service_name

        self.scontrol = None
        self.ccontrol = None
        self.sinterrupt = None
        self.cinterrupt = None

        self.init_device()
        self.init_profile()
        self.ensure_dbus_conf_file()

        bus_name = dbus.service.BusName("org.gcc.btservice", bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/org/gcc/btservice")

    # configure the bluetooth hardware device
    def init_device(self):
        print("Bringing hcio up")
        os.system("hciconfig hcio up")
        time.sleep(1)  # Waiting for BT device to be brought up - it would be nicer to find better way than arbitrary wait

        os.system("hciconfig hcio class 0x{:06x}".format(self.device_class))
        os.system("hciconfig hcio name " + self.device_name)
        os.system("hciconfig hcio piscan")

    def ensure_dbus_conf_file(self):
        def compare_old_and_new(old):
            with open("/etc/dbus-1/system.d/" + self.service_name + ".conf", "r") as etc_conf_file:
                original_conf_file_content = etc_conf_file.read()

            return original_conf_file_content == conf_file_content

        conf_file_content = "<!DOCTYPE busconfig PUBLIC \"-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN\" \"http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd\">"
        conf_file_content += "<busconfig>"
        conf_file_content += "        <policy user=\"root\">"
        conf_file_content += "                <allow own=\"" + self.service_name + "\"/>"
        conf_file_content += "        </policy>"
        conf_file_content += "        <policy context=\"default\">"
        conf_file_content += "                <deny own=\"" + self.service_name + "\"/>"
        conf_file_content += "                <allow send_destination=\"" + self.service_name + "\"/>"
        conf_file_content += "        </policy>"
        conf_file_content += "</busconfig>"

        config_exists = os.path.exists("/etc/dbus-1/system.d/" + self.service_name + ".conf")

        do_replace = not config_exists or not compare_old_and_new(conf_file_content)

        if do_replace:
            try:
                with open("/etc/dbus-1/system.d/" + self.service_name + ".conf", "w") as etc_conf_file:
                    etc_conf_file.write(conf_file_content)
            except Exception as e:
                sys.exit("Failed to create/replace " + self.service_name + ".conf in /etc/dbus-1/system.d/;" + str(e))

    def init_profile(self):
        service_record = self.sdp_service_record()

        opts = {
            "ServiceRecord": service_record,
            "Role": "server",
            "RequireAuthentication": False,
            "RequireAuthorization": False
        }

        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")

        manager.RegisterProfile(BTDevice.PROFILE_DBUS_PATH, self.uuid, opts)

    @staticmethod
    def sdp_service_record():
        print("Creating service record")

        hid_descriptor = hid_report_descriptor.create_joystick_report_descriptor(kind=hid_report_descriptor.GamePad, axes=(hid_report_descriptor.X, hid_report_descriptor.Y, hid_report_descriptor.Rx, hid_report_descriptor.Ry), button_number=14)
        record = sdp_record.create_simple_HID_SDP_Report("A Virtual Gamepad Controller", "Keyboard > BT Gamepad", "GCC", hid_descriptor, subclass=sdp_record.Gamepad)

        return record.xml()

    def listen(self):
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)

        self.scontrol.bind((socket.BDADDR_ANY, self.P_CTRL))
        self.sinterrupt.bind((socket.BDADDR_ANY, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol, cinfo = self.scontrol.accept()
        print("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print("Got a connection on the interrupt channel from " + cinfo[0])

    def send_message(self, message):
        self.cinterrupt.send(message)


if __name__ == "__main__":
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")

    DBusGMainLoop(set_as_default=True)

    bt = BTDevice()
    joystick = Joystick()

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

            joystick_axis = joystick.readAxis()
            joystick_buttons = joystick.readButtons()

            new_axis[0] = joystick_axis['x']
            new_axis[1] = joystick_axis['y']
            new_axis[2] = joystick_axis['rx']
            new_axis[3] = joystick_axis['ry']

            new_button_bits_1 = 0
            new_button_bits_2 = 0

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
