
# Usage Page
GenericDesktopCtrls = 0x01
Button = 0x09

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
        super(UsageMinimum, self).__init__(0x19, value)


class UsageMaximum(_SimpleElement):
    def __init__(self, value):
        super(UsageMaximum, self).__init__(0x29, value)


class LogicalMinimum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMinimum, self).__init__(0x15, value)


class LogicalMaximum(_SimpleElement):
    def __init__(self, value):
        super(LogicalMaximum, self).__init__(0x25, value)


class ReportCount(_SimpleElement):
    def __init__(self, count):
        super(ReportCount, self).__init__(0x95, count)


class ReportSize(_SimpleElement):
    def __init__(self, size):
        super(ReportSize, self).__init__(0x75, size)


class Input(_SimpleElement):
    def __init__(self, *options):
        super(Input, self).__init__(0x81, sum(options))


if __name__ == "__main__":

    # Testing creation of USB HID Report Descriptor

    descriptor = USBHIDReportDescriptor(
        UsagePage(GenericDesktopCtrls),
        Usage(GamePad),
        Collection(Application,
                   Collection(Report,
                              ReportID(InputReport),
                              UsagePage(Button),
                              UsageMinimum(0x01),
                              UsageMaximum(0x02),
                              LogicalMinimum(0),
                              LogicalMaximum(1),
                              ReportCount(14),
                              ReportSize(1),
                              Input(Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                              ReportCount(1),
                              ReportSize(2),
                              Input(Const, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                              Collection(Physical,
                                         UsagePage(GenericDesktopCtrls),
                                         Usage(X),
                                         Usage(Y),
                                         Usage(Rx),
                                         Usage(Ry),
                                         LogicalMinimum(-127),
                                         LogicalMaximum(127),
                                         ReportSize(8),
                                         ReportCount(4),
                                         Input(Data, Var, Abs, NoWrap, Linear, PreferredState, NoNullPosition),
                              )
                   )
        )
    )

    print("Descriptor bytes: " + (descriptor.hex()))
