
# Usage Page
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

# Usage
Pointer = 0x01
Mouse = 0x02
Value_0x03 = 0x03
Joystick = 0x04
GamePad = 0x05
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

# Collection
Physical = 0x00
Application = 0x01
Value_0x02 = 0x02
Report = 0x03

# Input
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

# Report Type
InputReport = 0x01
OutputReport = 0x02
FeatureReport = 0x03


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
    def __init__(self, code, value):
        self.code = code
        self.value = value if 0 <= value <= 255 else (256 + value)

    def values(self):
        yield self.code
        yield self.value


class UsagePage(_SimpleElement):
    def __init__(self, kind):
        super(UsagePage, self).__init__(0x05, kind)


class Usage(_SimpleElement):
    def __init__(self, kind):
        super(Usage, self).__init__(0x09, kind)


class ReportID(_SimpleElement):
    def __init__(self, report_type):
        super(ReportID, self).__init__(0x85, report_type)


class UsageMinimum(_SimpleElement):
    def __init__(self, value):
        super(UsageMinimum, self).__init__(0x19, value)  # TODO if value is less than -128 or over 127 it is code 0x1A and two bytes - little endian


class UsageMaximum(_SimpleElement):
    def __init__(self, value):
        super(UsageMaximum, self).__init__(0x29, value)  # TODO if value is less than -128 or over 127 it is code 0x2A and two bytes - little endian


class LogicalMinimum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMinimum, self).__init__(0x15, value)  # TODO if value is less than -128 or over 127 it is code 0x16 and two bytes - little endian


class LogicalMaximum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMaximum, self).__init__(0x25, value)  # TODO if value is less than -128 or over 127 it is code 0x26 and two bytes - little endian


class ReportCount(_SimpleElement):
    def __init__(self, count):
        super(ReportCount, self).__init__(0x95, count)


class ReportSize(_SimpleElement):
    def __init__(self, size):
        super(ReportSize, self).__init__(0x75, size)


class Input(_SimpleElement):
    def __init__(self, *options):
        super(Input, self).__init__(0x81, sum(options))


def create_joystick_report_descriptor(kind=GamePad, axes=(X, Y, Rx, Ry), button_number=14):
    input_report = [ReportID(InputReport)]
    input_report += [UsagePage(Button),
                     UsageMinimum(1),
                     UsageMaximum(button_number),
                     LogicalMinimum(0),
                     LogicalMaximum(1),
                     ReportCount(button_number),
                     ReportSize(1),
                     Input(Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
]
    if button_number % 8 != 0:
        input_report += [ReportCount(1),
                         ReportSize(8 - button_number % 8),
                         Input(Const, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition)]

    if axes is not None and len(axes) > 0:
        axes_collection = [UsagePage(GenericDesktopCtrls)]
        axes_collection += [Usage(axis) for axis in axes]
        axes_collection += [LogicalMinimum(-127),
                            LogicalMaximum(127),
                            ReportSize(8),
                            ReportCount(len(axes)),
                            Input(Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition)
                            ]

        input_report += [Collection(Physical, *axes_collection)]

    report = USBHIDReportDescriptor(
            UsagePage(GenericDesktopCtrls),
            Usage(kind),
            Collection(Application, Collection(Report, *input_report))
        )

    print(report.hex())

    return report


if __name__ == "__main__":

    # Testing creation of USB HID Report Descriptor

    descriptor = create_joystick_report_descriptor(kind=GamePad, axes=(X, Y, Rx, Ry), button_number=14)

    print("Descriptor bytes: " + (descriptor.hex()))
