#
# Copyright 2019 Games Creators Club
#
# MIT License
#

# Major Service Class

LIMITED_DISCOVERABLE_MODE = 0x2000
POSITIONING = 0x10000
NETWORKING = 0x20000
RENDERING = 0x40000
CAPTURING = 0x80000
OBJECT_TRANSFER = 0x100000
AUDIO = 0x200000
TELEPHONY = 0x400000
INFORMATION = 0x800000

# Major Device Class

COMPUTER = 0x100
PHONE = 0x200
LAN_NETWORK = 0x300
AUDIO_VIDEO = 0x400
PERIPHERAL = 0x500
IMAGING = 0x600
WEARABLE = 0x700
TOY = 0x800
UNCATOGORIZED = 0x1F00

# Minor Device Class Computer

DESKTOP_WORKSTATION = 0x4
SERVER = 0x8
LATOP = 0xC
HANDHELD = 0x10
PALMSIZED = 0x14
WEARABLE_WATCH = 0x18

# Minor Device Class Phone

CELLULAR = 0x4
CORDLESS = 0x8
SMART_PHONE = 0xC
WIREDMODEM_OR_VOICE_GATEWAY = 0x10
COMMON_ISDN_ACCESS = 0x14

# Minor Device Class LAN

LAN_FULLY_AVAILABLE = 0x0
LAN_1_17_AVAILABLE = 0x20
LAN_17_33_AVAILABLE = 0x40
LAN_33_50_AVAILABLE = 0x60
LAN_50_67_AVAILABLE = 0x80
LAN_67_83_AVAILABLE = 0xA0
LAN_83_99_AVAILABLE = 0xC0
LAN_NO_SERVICE_AVAILABLE = 0xE0

# Minor Device Class Audio/Video

WEARABLE_HEADSET = 0x4
HANDS_FREE = 0x8
MICROPHONE = 0x10
LOUDSPEAKER = 0x14
HEADPHONES = 0x18
PORTABLE_AUDIO = 0x1C
CAR_AUDIO = 0x20
SET_TOP_BOX = 0x24
HIFI_AUDIO_DEVICE= 0x28
VCR = 0x2C
VIDEO_CAMERA = 0x30
CAMCORDER = 0x34
VIDEO_MONITOR = 0x38
VIDEO_DISPLAY_AND_LOUDSPEAKER = 0x3C
VIDEO_CONFERENCING = 0x40
GAMING_OR_TOY = 0x44

# Minor Device Class Peripheral (Mouse, Joystick, Keyboard)

KEYBOARD = 0x40
POINTING_DEVICE = 0x80
COMBO_KEYBOARD_POINTING_DEVICE = 0xC0

JOYSTICK = 0x4
GAMEPAD = 0x8
REMOTE_CONTROL = 0xC
SENSING_DEVICE = 0x10
DIGITIZER_TABLED = 0x14
CARD_READER = 0x18

# Minor Device Class Imaging

DISPLAY = 0x10
CAMERA = 0x20
SCANNER = 0x40
PRINTER = 0x80

# Minor Device Class Wearable

WRIST_WATCH = 0x4
PAGER = 0x8
JACKET = 0xC
HELMET = 0x10
GLASSES = 0x14

# Minor Device Class Toy

ROBOT = 0x4
VEHILCE = 0x8
DOLL_OR_ACTION_FIGURE = 0xC
CONTROLLER = 0x10
GAME = 0x14
