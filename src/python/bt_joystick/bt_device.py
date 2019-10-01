#!/usr/bin/env python3

#
# Copyright 2019 Games Creators Club
#
# MIT License
#

# Based on https://github.com/yaptb/BlogCode

from optparse import OptionParser

import os
import sys
import time
import socket

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from bt_joystick import sdp_record
from bt_joystick import hid_report_descriptor

from bt_joystick.bt_device_classes import LIMITED_DISCOVERABLE_MODE, PERIPHERAL, GAMEPAD
from bt_joystick.hid_report_descriptor import Usage
from bt_joystick.sdp_record import MinorDeviceClass


ADAPTER_INTERFACE = 'org.bluez.Adapter1'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = '/org/gcc/btservice'


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


class BTDevice(dbus.service.Object):
    P_CTRL = 17  # Service port - must match port configured in SDP record
    P_INTR = 19  # Service port - must match port configured in SDP record#Interrrupt port
    PROFILE_DBUS_PATH = "/bluez/gcc/gcc_joy_profile"  # dbus path of  the bluez profile we will create

    def __init__(self, device_name='gcc-bt-joystick',
                 device_class=LIMITED_DISCOVERABLE_MODE | PERIPHERAL | GAMEPAD,
                 uuid="00001124-0000-1000-8000-00805f9b34fb",
                 service_name='org.gcc.btservice',
                 service_record=None,
                 hid_descriptor=None):

        self.device_name = device_name
        self.device_class = device_class
        self.uuid = uuid
        self.service_name = service_name

        self.scontrol = None
        self.ccontrol = None
        self.sinterrupt = None
        self.cinterrupt = None

        self.pairable = False

        # create default HID descriptor and SDP record if not specified
        if service_record is not None:
            self.service_record = service_record
        else:
            if hid_descriptor is None:
                hid_descriptor = hid_report_descriptor.create_joystick_report_descriptor(kind=Usage.Gamepad, axes=(Usage.X, Usage.Y, Usage.Rx, Usage.Ry), button_number=14)
            self.service_record = sdp_record.create_simple_HID_SDP_Report("A Virtual Gamepad Controller", "Keyboard > BT Gamepad", "GCC", hid_descriptor, subclass=MinorDeviceClass.Gamepad)

        self.init_device()
        self.init_profile()
        self.ensure_dbus_conf_file()

        self.system_bus = dbus.SystemBus()
        obj = self.system_bus.get_object('org.bluez', "/org/bluez")
        manager = dbus.Interface(obj, "org.bluez.AgentManager1")

        dbus.service.Object.__init__(self, self.system_bus, AGENT_PATH)
        manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")  # Capability can be DisplayOnly or DisplayYesNo, KeyboardOnly or KeyboardDisplay or just NoInputNoOutput
        manager.RequestDefaultAgent(AGENT_PATH)
        print("Agent registered ")

    def init_device(self):
        # configure the bluetooth hardware device
        print("Bringing hcio up")
        os.system("hciconfig hcio up")
        time.sleep(1)  # Waiting for BT device to be brought up - it would be nicer to find better way than arbitrary wait

        os.system("hciconfig hcio class 0x{:06x}".format(self.device_class))
        os.system("hciconfig hcio name " + self.device_name)
        # os.system("hciconfig hcio piscan")

    def ensure_dbus_conf_file(self):
        def compare_old_and_new(old_content):
            with open("/etc/dbus-1/system.d/" + self.service_name + ".conf", "r") as existing_etc_conf_file:
                original_conf_file_content = existing_etc_conf_file.read()

            return original_conf_file_content == old_content

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
            except Exception as e1:
                sys.exit("Failed to create/replace " + self.service_name + ".conf in /etc/dbus-1/system.d/;" + str(e1))

    def init_profile(self):
        opts = {
            "ServiceRecord": self.service_record.xml(),
            "Role": "server",
            "RequireAuthentication": False,
            "RequireAuthorization": False
        }

        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")

        manager.RegisterProfile(BTDevice.PROFILE_DBUS_PATH, self.uuid, opts)

    def listen(self, timeout):
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)

        self.scontrol.settimeout(timeout)
        self.sinterrupt.settimeout(timeout)

        self.scontrol.bind((socket.BDADDR_ANY, self.P_CTRL))
        self.sinterrupt.bind((socket.BDADDR_ANY, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)

        try:
            self.ccontrol, cinfo = self.scontrol.accept()
            print("Got a connection on the control channel from " + cinfo[0])

            self.cinterrupt, cinfo = self.sinterrupt.accept()
            print("Got a connection on the interrupt channel from " + cinfo[0])
            return True
        except socket.timeout as e:
            return False

    def send_message(self, message):
        self.cinterrupt.send(message)

    def send_values(self, button_bits, axis_values, hat_value):
        """
        Convenience function to send a message with button states, axis values and hat switch state
        :param button_bits: bitmap for the button states, an integer with at most 16 bits
        :param axis_values: list of axis values (each in -127..127)
        :param hat_value: value for the hat switch: 1..8 for top, top right, right, ..., top left, or 9 for the middle (not pressed) position
        """
        self.send_message(bytes((0xA1, 0x01, button_bits & 255, button_bits >> 8, *[v if v >= 0 else v + 256 for v in axis_values], hat_value)))

    def allow_pairing(self, pairable):
        self.pairable = pairable

    def is_pairable_allowed(self):
        return self.pairable

    def set_discoverable(self, discoverable):
        props = dbus.Interface(self.system_bus.get_object("org.bluez", "/org/bluez/hci0"), "org.freedesktop.DBus.Properties")
        props.Set(ADAPTER_INTERFACE, "Discoverable", dbus.types.Boolean(discoverable))

    # Agent methods

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        print("Release")
        # if self.exit_on_release:
        #     #mainloop.quit()
        #     pass

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        print("AuthorizeService (%s, %s)" % (device, uuid))
        # authorize = ask("Authorize connection (yes/no): ")
        # if authorize == "yes":
        #     return
        # raise Rejected("Connection rejected by user")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print("RequestPinCode (%s)" % (device))
        # set_trusted(device)
        # return ask("Enter PIN Code: ")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print("RequestPasskey (%s)" % (device))
        # set_trusted(device)
        # passkey = ask("Enter passkey: ")
        # return dbus.UInt32(passkey)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        print("DisplayPasskey (%s, %06u entered %u)" %
              (device, passkey, entered))

    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def DisplayPinCode(self, device, pincode):
        print("DisplayPinCode (%s, %s)" % (device, pincode))

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print("RequestConfirmation (%s, %06d) ..." % (device, passkey))
        if not self.pairable:
            print("Rejecting as we are not pairable")
            raise Rejected("Try again")

        print("Setting device to trusted...")
        props = dbus.Interface(self.system_bus.get_object("org.bluez", device), "org.freedesktop.DBus.Properties")
        props.Set("org.bluez.Device1", "Trusted", True)
        print("Approving device...")

        return

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print("RequestAuthorization (%s)" % (device))
        # auth = ask("Authorize? (yes/no): ")
        # if auth == "yes":
        #     return
        # raise Rejected("Pairing rejected")

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Cancel(self):
        print("Cancel")
