#!/usr/bin/python

###!/usr/bin/env python3

# Based on https://github.com/yaptb/BlogCode


from __future__ import absolute_import, print_function

import os
import sys
import dbus
import dbus.service
import time
import random
from bluetooth import *

from dbus.mainloop.glib import DBusGMainLoop


class BTBluezProfile(dbus.service.Object):
    fd = -1

    @dbus.service.method("org.bluez.Profile1", in_signature="", out_signature="")
    def Release(self):
        print("Release")
        mainloop.quit()

    @dbus.service.method("org.bluez.Profile1", in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")

    @dbus.service.method("org.bluez.Profile1", in_signature="oha{sv}", out_signature="")
    def NewConnection(self, path, fd, properties):
        self.fd = fd.take()
        print("NewConnection(%s, %d)" % (path, self.fd))
        for key in properties.keys():
            if key == "Version" or key == "Features":
                print("  %s = 0x%04x" % (key, properties[key]))
            else:
                print("  %s = %s" % (key, properties[key]))

    @dbus.service.method("org.bluez.Profile1", in_signature="o", out_signature="")
    def RequestDisconnection(self, path):
        print("RequestDisconnection(%s)" % path)

        if self.fd > 0:
            os.close(self.fd)
            self.fd = -1

    def __init__(self, bus, path):
        dbus.service.Object.__init__(self, bus, path)


class BTDevice:
    MY_ADDRESS = "B8:27:EB:68:71:C7"
    MY_DEV_NAME = "gcc-bt-joystick"

    P_CTRL = 17  # Service port - must match port configured in SDP record
    P_INTR = 19  # Service port - must match port configured in SDP record#Interrrupt port
    PROFILE_DBUS_PATH = "/bluez/gcc/gcc_joy_profile"  # dbus path of  the bluez profile we will create
    SDP_RECORD_PATH = sys.path[0] + "/sdp_record_gamepad.xml"  # file path of the sdp record to laod
    UUID = "00001124-0000-1000-8000-00805f9b34fb"

    def __init__(self):
        print("Setting up BT device")
        self.scontrol = None
        self.ccontrol = None
        self.sinterrupt = None
        self.cinterrupt = None

        self.init_bt_device()
        self.init_bluez_profile()

    # configure the bluetooth hardware device
    @staticmethod
    def init_bt_device():
        print("Configuring for name " + BTDevice.MY_DEV_NAME)

        # set the device class to a keybord and joystick
        print("Bringing hcio up")
        os.system("hciconfig hcio up")
        time.sleep(1)

        print("Setting up hcio")
        os.system("hciconfig hcio class 0x002508")
        os.system("hciconfig hcio name " + BTDevice.MY_DEV_NAME)
        os.system("hciconfig hcio piscan")

    # set up a bluez profile to advertise device capabilities from a loaded service record
    def init_bluez_profile(self):

        print("Configuring Bluez Profile")

        # setup profile options
        service_record = self.read_sdp_service_record()

        opts = {
            "ServiceRecord": service_record,
            "Role": "server",
            "RequireAuthentication": False,
            "RequireAuthorization": False
        }

        # retrieve a proxy for the bluez profile interface
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")

        profile = BTBluezProfile(bus, BTDevice.PROFILE_DBUS_PATH)

        manager.RegisterProfile(BTDevice.PROFILE_DBUS_PATH, BTDevice.UUID, opts)

        print("Profile registered ")

    # read and return an sdp record from a file
    @staticmethod
    def read_sdp_service_record():
        print("Reading service record")

        try:
            with open(BTDevice.SDP_RECORD_PATH, "r") as fh:
                return fh.read()
        except Exception as e:
            sys.exit("Could not open the sdp record. Exiting..." + str(e))

    # ideally this would be handled by the Bluez 5 profile
    # but that didn't seem to work
    def listen(self):

        print("Waiting for connections")
        self.scontrol = BluetoothSocket(L2CAP)
        self.sinterrupt = BluetoothSocket(L2CAP)

        # bind these sockets to a port - port zero to select next available
        self.scontrol.bind((self.MY_ADDRESS, self.P_CTRL))
        self.sinterrupt.bind((self.MY_ADDRESS, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol, cinfo = self.scontrol.accept()
        print("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print("Got a connection on the interrupt channel from " + cinfo[0])

    # send a string to the bluetooth host machine
    def send_string(self, message):

        #    print("Sending "+message)
        self.cinterrupt.send(message)


# define a dbus service that emulates a bluetooth keyboard
# this will enable different clients to connect to and use
# the service
class BTService(dbus.service.Object):

    def __init__(self):
        print("Setting up service")
        self.ensure_dbus_conf_file()

        bus_name = dbus.service.BusName("org.gcc.btservice", bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/org/gcc/btservice")

        self.device = BTDevice()

    def start_listening(self):
        self.device.listen()

    @staticmethod
    def ensure_dbus_conf_file():
        if not os.path.exists("/etc/dbus-1/system.d/org.gcc.btservice.conf"):
            try:
                with open(sys.path[0] + "/org.gcc.btservice.conf", "r") as conf_file:
                    conf_file_content = conf_file.read()

                with open("/etc/dbus-1/system.d/org.gcc.btservice.conf", "w") as etc_conf_file:
                    etc_conf_file.write(conf_file_content)

            except Exception as e:
                sys.exit("Failed to copy org.gcc.btservice.conf to /etc/dbus-1/system.d/;" + str(e))

    @dbus.service.method('org.gcc.btservice', in_signature='yay')
    def send_keys(self, modifier_byte, keys):

        cmd_str = ""
        cmd_str += chr(0xA1)
        cmd_str += chr(0x01)
        cmd_str += chr(modifier_byte)
        cmd_str += chr(0x00)

        count = 0
        for key_code in keys:
            if count < 6:
                cmd_str += chr(key_code)
            count += 1

        self.device.send_string(cmd_str)

    def send_input(self, inp):
        str_inp = ""
        for elem in inp:
            if type(elem) is list:
                tmp_str = ""
                for tmp_elem in elem:
                    tmp_str += str(tmp_elem)
                for i in range(0, len(tmp_str) // 8):
                    if (i + 1) * 8 >= len(tmp_str):
                        str_inp += chr(int(tmp_str[i*8:], 2))
                    else:
                        str_inp += chr(int(tmp_str[i * 8:(i + 1) * 8], 2))
            else:
                str_inp += chr(elem)

        self.device.send_string(str_inp)


if __name__ == "__main__":
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")

    DBusGMainLoop(set_as_default=True)

    bt = BTService()

    while True:
        re_start = False
        bt.start_listening()

        button_bits_1 = 0
        button_bits_2 = 0

        axis = [0, 0, 0, 0]

        while not re_start:
            time.sleep(1)

            change_axis = random.randint(0, 3)
            change_value = random.randint(0, 10)

            v = (axis[change_axis] + change_value) % 255
            if v < 0:
                v = 256 - v

            axis[change_axis] = v

            data = [0xA1, 0x01, button_bits_1, button_bits_2, axis[0], axis[1], axis[2], axis[3]]

            print("Changing data " + str(data) + "; changed axis " + str(change_axis) + " for " + str(change_value) + " and got " + str(v))
            try:
                bt.send_input(data)
            except Exception as e:
                print("Failed to send data - disconnected " + str(e))
                re_start = True
