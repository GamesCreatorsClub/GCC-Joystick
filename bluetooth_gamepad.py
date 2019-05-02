#!/usr/bin/env python3

# Based on https://github.com/yaptb/BlogCode

import os
import sys
import dbus
import dbus.service
import time
import socket

import sdp_record
import usb_hid_report_descriptor

from bluetooth import *
from dbus.mainloop.glib import DBusGMainLoop
from smbus import SMBus
from joystick import Joystick
from sdp_record import SDPRecord, ServiceClassIDList, ProtocolDescriptorList, BrowseGroupList, LanguageBaseAttributeIDList, BluetoothProfileDescriptorList, AdditionalProtocolDescriptorLists, \
    ServiceName, ServiceDescription, ProviderName, HIDDeviceReleaseNumber, HIDProfileVersion, HIDDeviceSubclass, HIDCountryCode, HIDVirtualCable, HIDReconnectInitiate, HIDLANGIDBaseList, \
    HIDDescriptorList, HIDParserVersion, HIDSupervisionTimeout, HIDNormallyConnectable, HIDBootDevice, HIDSSRHostMaxLatency, HIDSSRHostMinTimeout, HumanInterfaceDeviceService, Sequence, UUID, L2CAP, \
    UInt16, HIDP, PublicBrowseGroup, LanguageBase, HID_Interrupt, HIDLANGIDBase
from usb_hid_report_descriptor import UsagePage, Usage, Collection, GenericDesktopCtrls, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition, \
    Application, Report, ReportID, InputReport, UsageMinimum, UsageMaximum, LogicalMinimum, LogicalMaximum, ReportCount, ReportSize, Input, Const, Physical


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
        service_record = self.sdp_service_record()

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

    # ideally this would be handled by the Bluez 5 profile
    # but that didn't seem to work
    def listen(self):

        print("Waiting for connections")
        self.scontrol = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)
        self.sinterrupt = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_L2CAP)

        # bind these sockets to a port - port zero to select next available
        self.scontrol.bind((socket.BDADDR_ANY, self.P_CTRL))
        self.sinterrupt.bind((socket.BDADDR_ANY, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(1)  # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol, cinfo = self.scontrol.accept()
        print("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print("Got a connection on the interrupt channel from " + cinfo[0])

    # send a message to the bluetooth host machine
    def send_message(self, message):

        #    print("Sending "+message)
        self.cinterrupt.send(message)

    @staticmethod
    def sdp_service_record():
        print("Creating service record")

        record = SDPRecord()

        record += ServiceClassIDList(HumanInterfaceDeviceService)
        record += ProtocolDescriptorList(Sequence(UUID(L2CAP), UInt16(HIDP)), Sequence(UUID(HIDP)))
        record += BrowseGroupList(UUID(PublicBrowseGroup))
        record += LanguageBaseAttributeIDList(LanguageBase('en', 0x006a, 0x0100))  # 'en' (0x656e), 0x006A is UTF-8 encoding, 0x0100 represents attribute ID offset used for ServiceName, ServiceDescriptor and ProviderName attributes!
        record += BluetoothProfileDescriptorList(Sequence(UUID(HumanInterfaceDeviceService), UInt16(0x0100)))  # 0x0100 indicating version 1.0
        record += AdditionalProtocolDescriptorLists(Sequence(Sequence(UUID(L2CAP), UInt16(HID_Interrupt)), Sequence(UUID(HIDP))))
        record += ServiceName(0x0100, "A Virtual Gamepad Controller")  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
        record += ServiceDescription(0x0100, "Keyboard > BT Gamepad")  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
        record += ProviderName(0x0100, "GCC")  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
        record += HIDDeviceReleaseNumber(0x100)  # deprecated release number 1.0
        record += HIDProfileVersion(0x0111)  # indicating version 1.11
        record += HIDDeviceSubclass(sdp_record.Gamepad)
        record += HIDCountryCode(0x00)
        record += HIDVirtualCable(False)
        record += HIDReconnectInitiate(False)
        record += HIDLANGIDBaseList(HIDLANGIDBase(0x0409, 0x0100))  # 0x0409 per http://info.linuxoid.in/datasheets/USB%202.0a/USB_LANGIDs.pdf is English (United States)
        record += HIDDescriptorList(report=usb_hid_report_descriptor.USBHIDReportDescriptor(
            UsagePage(GenericDesktopCtrls),
            Usage(usb_hid_report_descriptor.GamePad),
            Collection(usb_hid_report_descriptor.Application,
                       Collection(usb_hid_report_descriptor.Report,
                                  ReportID(InputReport),
                                  UsagePage(usb_hid_report_descriptor.Button),
                                  UsageMinimum(0x01),
                                  UsageMaximum(0x02),
                                  LogicalMinimum(0),
                                  LogicalMaximum(1),
                                  ReportCount(14),
                                  ReportSize(1),
                                  Input(usb_hid_report_descriptor.Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                                  ReportCount(1),
                                  ReportSize(2),
                                  Input(Const, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                                  Collection(Physical,
                                             UsagePage(GenericDesktopCtrls),
                                             Usage(usb_hid_report_descriptor.X),
                                             Usage(usb_hid_report_descriptor.Y),
                                             Usage(usb_hid_report_descriptor.Rx),
                                             Usage(usb_hid_report_descriptor.Ry),
                                             LogicalMinimum(-127),
                                             LogicalMaximum(127),
                                             ReportSize(8),
                                             ReportCount(4),
                                             Input(usb_hid_report_descriptor.Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                                             )
                                  )
                       )
        ).hex().lower(), encoding="hex")
        record += HIDParserVersion(0x0100)  # 1.0
        record += HIDSupervisionTimeout(0x0c80)  # 3200
        record += HIDNormallyConnectable(True)
        record += HIDBootDevice(False)
        record += HIDSSRHostMaxLatency(0x0640)  # 1600
        record += HIDSSRHostMinTimeout(0x0320)  # 800

        return record.xml()


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

    def send_input(self, inp):
        self.device.send_message(inp)


if __name__ == "__main__":
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")

    DBusGMainLoop(set_as_default=True)

    bt = BTService()
    joystick = Joystick()

    while True:
        re_start = False
        bt.start_listening()

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

                # print("Changing data " + str(data) + "; changed axis " + str(change_axis) + " for " + str(change_value) + " and got " + str(v))
                try:
                    bt.send_input(data)
                except Exception as e:
                    print("Failed to send data - disconnected " + str(e))
                    re_start = True
