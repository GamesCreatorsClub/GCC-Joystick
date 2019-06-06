#
# Copyright 2019 Games Creators Club
#
# MIT License
#


class _Element:
    def values(self):
        raise NotImplemented

    def __bytes__(self):
        return bytes(self.values())


class _Elements(_Element):
    def __init__(self, *elements):
        self.elements = elements

    def values(self):
        for e in self.elements:
            for b in e.values():
                if b < 0 or b > 255:
                    print("B=" + str(b))
                yield b

    def hex(self):
        return "".join("{:02x}".format(x) for x in bytes(self))


class USBHIDReportDescriptor(_Elements):
    def __init__(self, *args):
        super(USBHIDReportDescriptor, self).__init__(*args)


class Collection(_Elements):
    Physical = 0x00
    Application = 0x01
    Value_0x02 = 0x02
    Report = 0x03

    def __init__(self, kind, *elements):
        super(Collection, self).__init__(*elements)
        self.kind = kind

    def values(self):
        yield 0xA1
        yield self.kind
        for b in super(Collection, self).values():
            yield b
        yield 0xc0


class _SimpleElement(_Element):
    UsagePage = 0x04
    Usage = 0x08
    UsageMinimum = 0x18
    UsageMaximum = 0x28
    LogicalMinimum = 0x14
    LogicalMaximum = 0x24
    PhysicalMinimum = 0x34
    PhysicalMaximum = 0x44
    Unit = 0x64
    ReportSize = 0x74
    Input = 0x80
    ReportID = 0x84
    ReportCount = 0x94

    def __init__(self, code, value):
        self.code = code
        if -127 <= value < 0:
            self.value = value + 256
        elif -32768 <= value < -255:
            self.value = value + 65536
        elif -0x80000000 <= value < -32768:
            self.value = value + 0x100000000
        else:
            self.value = value

    def values(self):
        # Handle two different sizes: 1 byte for -127..127, and 2 for -255..255
        # (assuming the supplied code is for the first one, so adding 1 to it specifies the 2-byte version
        # - the first two bits in the code actually specify the size)
        if self.value is None:
            yield self.code
        elif self.value > 65535:
            yield self.code + 3
            yield self.value & 255
            yield (self.value >> 8) & 255
            yield (self.value >> 16) & 255
            yield (self.value >> 24) & 255
        elif self.value > 255:
            yield self.code + 2
            yield self.value & 255
            yield self.value >> 8
        else:
            yield self.code + 1
            yield self.value


class UsagePage(_SimpleElement):
    GenericDesktopCtrls = 0x01
    SimCtrl = 0x02
    VRCtrls = 0x03
    SportCtrls = 0x04
    GameCtrls = 0x05
    GenericDevCtrls = 0x06
    KeyboardKeypad = 0x07
    LEDS = 0x08
    Button = 0x09
    Ordinal = 0x0A
    Telephony = 0x0B
    Consumer = 0x0C
    Digitizer = 0x0D
    PIDPage = 0x0F
    Unicode = 0x10
    AlphanumericDisplay = 0x14

    def __init__(self, kind):
        super(UsagePage, self).__init__(_SimpleElement.UsagePage, kind)


class Usage(_SimpleElement):
    Pointer = 0x01
    Mouse = 0x02
    Value_0x03 = 0x03
    Joystick = 0x04
    Gamepad = 0x05
    Keyboard = 0x06
    Keypad = 0x07
    MultiAxisController = 0x08
    X = 0x30
    Y = 0x31
    Z = 0x32
    Rx = 0x33
    Ry = 0x34
    Rz = 0x35
    Slider = 0x36
    Dial = 0x37
    Wheel = 0x38
    HatSwitch = 0x39
    CountedBuffer = 0x3A
    ByteCount = 0x3B
    MotionWakeup = 0x3C
    Start = 0x3D
    Vx = 0x40
    Vy = 0x41
    Vz = 0x42
    Vbrx = 0x43
    Vbry = 0x44
    Vbrz = 0x45
    Vno = 0x046
    FeatureNotification = 0x47
    SysControl = 0x80
    SysPowerDown = 0x81
    SysSleep = 0x82
    SysWakeUp = 0x83
    SysContextMenu = 0x84
    SysMainMenu = 0x85
    SysAppMenu = 0x86
    SysMenuHelp = 0x87
    SysMenuExit = 0x88
    SysMenuSelect = 0x89
    SysMenuRight = 0x8A
    SysMenuLeft = 0x8B
    SysMenuUp = 0x8C
    SysMenuDown = 0x8D
    SysColdRestart = 0x8E
    SysWarmRestart = 0x8F
    DPadUp = 0x90
    DPadDown = 0x91
    DPadRight = 0x92
    DPadLeft = 0x93
    SysDock = 0xA0
    SysUndock = 0xA1
    SysSetup = 0xA2
    SysBreak = 0xA3
    SysDebuggerBreak = 0xA4
    ApplicationBreak = 0xA5
    ApplicationDebuggerBreak = 0xA6
    SysSpeakerMute = 0xA7
    SysHibernate = 0xA8
    SysDisplayInvert = 0xB0
    SysDisplayInternal = 0xB1
    SysDisplayExternal = 0xB2
    SysDisplayBoth = 0xB3
    SysDisplayDual = 0xB4
    SysDisplayToggleIntExt = 0xB5
    SysDisplaySwap = 0xB6
    SysDisplayLCDAutoscale = 0xB7

    def __init__(self, kind):
        super(Usage, self).__init__(_SimpleElement.Usage, kind)


class ReportID(_SimpleElement):
    InputReport = 0x01
    OutputReport = 0x02
    FeatureReport = 0x03

    def __init__(self, report_type):
        super(ReportID, self).__init__(_SimpleElement.ReportID, report_type)


class UsageMinimum(_SimpleElement):
    def __init__(self, value):
        super(UsageMinimum, self).__init__(_SimpleElement.UsageMinimum, value)  # TODO if value is less than -128 or over 127 it is code 0x1A and two bytes - little endian


class UsageMaximum(_SimpleElement):
    def __init__(self, value):
        super(UsageMaximum, self).__init__(_SimpleElement.UsageMaximum, value)  # TODO if value is less than -128 or over 127 it is code 0x2A and two bytes - little endian


class LogicalMinimum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMinimum, self).__init__(_SimpleElement.LogicalMinimum, value)  # TODO if value is less than -128 or over 127 it is code 0x16 and two bytes - little endian


class LogicalMaximum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMaximum, self).__init__(_SimpleElement.LogicalMaximum, value)  # TODO if value is less than -128 or over 127 it is code 0x26 and two bytes - little endian


class PhysicalMinimum(_SimpleElement):
    def __init__(self, value):
        super(PhysicalMinimum, self).__init__(_SimpleElement.PhysicalMinimum, value)


class PhysicalMaximum(_SimpleElement):
    def __init__(self, value):
        super(PhysicalMaximum, self).__init__(_SimpleElement.PhysicalMaximum, value)


class ReportCount(_SimpleElement):
    def __init__(self, count):
        super(ReportCount, self).__init__(_SimpleElement.ReportCount, count)


class ReportSize(_SimpleElement):
    def __init__(self, size):
        super(ReportSize, self).__init__(_SimpleElement.ReportSize, size)


class Unit(_SimpleElement):
    EnglishRotationDegrees = 0x14
    CM = 0x11
    SIRad = 0x21

    def __init__(self, value):
        super(Unit, self).__init__(_SimpleElement.Unit, value)


class Input(_SimpleElement):
    Data = 0x00
    Const = 0x01

    Array = 0x00
    Var = 0x02

    Abs = 0x00
    Rel = 0x04

    NoWrap = 0x00
    Wrap = 0x08

    Linear = 0x00
    Nonlinear = 0x10

    PreferredState = 0x00
    NoPreferredState = 0x20

    NoNullPosition = 0x00
    NullState = 0x40

    def __init__(self, *options):
        super(Input, self).__init__(_SimpleElement.Input, sum(options))


def create_joystick_report_descriptor(kind=Usage.Gamepad, axes=(Usage.X, Usage.Y, Usage.Rx, Usage.Ry), hat_switch=False, button_number=14):
    input_report = [ReportID(ReportID.InputReport)]
    input_report += [UsagePage(UsagePage.Button),
                     UsageMinimum(1),
                     UsageMaximum(button_number),
                     LogicalMinimum(0),
                     LogicalMaximum(1),
                     ReportCount(button_number),
                     ReportSize(1),
                     Input(Input.Data, Input.Var, Input.Abs, Input.NoWrap, Input.Linear, Input.PreferredState, Input.NoNullPosition)
                     ]

    if button_number % 8 != 0:
        input_report += [ReportCount(1),
                         ReportSize(8 - button_number % 8),
                         Input(Input.Const, Input.Var, Input.Abs, Input.NoWrap, Input.Linear, Input.PreferredState, Input.NoNullPosition)]

    if axes is not None and len(axes) > 0:
        axes_collection = [UsagePage(UsagePage.GenericDesktopCtrls)]
        axes_collection += [Usage(axis) for axis in axes]
        axes_collection += [LogicalMinimum(-127),
                            LogicalMaximum(127),
                            ReportSize(8),
                            ReportCount(len(axes)),
                            Input(Input.Data, Input.Var, Input.Abs, Input.NoWrap, Input.Linear, Input.PreferredState, Input.NoNullPosition)
                            ]

        input_report += [Collection(Collection.Physical, *axes_collection)]

    if hat_switch:
        hat_collection = [UsagePage(UsagePage.GenericDesktopCtrls)]
        # 4 bits for the hat switch, 9 possible positions, 0..315 degrees
        hat_collection += [Usage(Usage.HatSwitch),
                           LogicalMinimum(0),
                           LogicalMaximum(8), #7
                           PhysicalMinimum(0),
                           PhysicalMaximum(315), #270), #315
                           Unit(Unit.EnglishRotationDegrees),
                           ReportSize(4),
                           ReportCount(1),
                           Input(Input.Var, Input.Abs, Input.NullState)]
        # pad 4 bits
        hat_collection += [ReportCount(1),
                           ReportSize(4),
                           Input(Input.Const, Input.Var, Input.Abs, Input.NoWrap, Input.Linear, Input.PreferredState, Input.NoNullPosition)]

        input_report += [Collection(Collection.Physical, *hat_collection)]

    report = USBHIDReportDescriptor(
            UsagePage(UsagePage.GenericDesktopCtrls),
            Usage(kind),
            Collection(Collection.Application, Collection(Collection.Report, *input_report))
        )

    print(report.hex())

    return report


if __name__ == "__main__":

    # Testing creation of USB HID Report Descriptor

    descriptor = create_joystick_report_descriptor(kind=Usage.Gamepad, axes=(Usage.X, Usage.Y, Usage.Rx, Usage.Ry), button_number=14)

    print("Descriptor bytes: " + (descriptor.hex()))
