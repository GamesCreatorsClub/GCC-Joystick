#
# Copyright 2019 Games Creators Club
#
# MIT License
#

# Protocol Identifiers; Channel Identifiers, Protocol and Service Multiplexers (PSMs)?
from functools import reduce


class Consts:
    # Channel Identifiers, Protocol and Service Multiplexers (PSMs)

    SDP = 0x0001  # Bluetooth Core Specification
    UDP = 0x0002  # [NO USE BY PROFILES]
    RFCOMM = 0x0003  # RFCOMM with TS 07.10
    TCP = 0x0004  # [NO USE BY PROFILES]
    TCS_BIN = 0x0005  # Telephony Control Specification / TCS Binary [DEPRECATED]
    TCS_AT = 0x0006  # [NO USE BY PROFILES]
    ATT = 0x0007  # Attribute Protocol
    TCS_BIN_CORDLESS = 0x0007  # See Bluetooth Telephony Control Specification / TCS Binary, Bluetooth SIG
    OBEX = 0x0008  # IrDA Interoperability
    IP = 0x0009  # [NO USE BY PROFILES]
    FTP = 0x000A  # [NO USE BY PROFILES]
    HTTP = 0x000C  # [NO USE BY PROFILES]
    WSP = 0x000E  # [NO USE BY PROFILES]
    BNEP = 0x000F  # Bluetooth Network Encapsulation Protocol (BNEP)
    UPNP = 0x0010  # Extended Service Discovery Profile (ESDP) [DEPRECATED]
    HIDP = 0x0011  # Human Interface Device Profile (HID)
    HID_Control = 0x0011  # See Human Interface Device, Bluetooth SIG
    HardcopyControlChannel = 0x0012  # Hardcopy Cable Replacement Profile (HCRP)
    HID_Interrupt = 0x0013  # See Human Interface Device, Bluetooth SIG
    HardcopyDataChannel = 0x0014  # See Hardcopy Cable Replacement Profile (HCRP)
    UPnP = 0x0015  # See [ESDP] , Bluetooth SIG
    HardcopyNotification = 0x0016  # Hardcopy Cable Replacement Profile (HCRP)
    AVCTP = 0x0017  # Audio/Video Control Transport Protocol (AVCTP)
    AVDTP = 0x0019  # Audio/Video Distribution Transport Protocol (AVDTP)
    CMTP = 0x001B  # Common ISDN Access Profile (CIP) [DEPRECATED]
    AVCTP_Browsing = 0x001B  # See Audio/Video Remote Control Profile, Bluetooth SIG
    UDI_C_Plane = 0x001D  # See the Unrestricted Digital Information Profile [UDI], Bluetooth SIG
    MCAPControlChannel = 0x001E  # Multi-Channel Adaptation Protocol (MCAP)
    MCAPDataChannel = 0x001F  # Multi-Channel Adaptaion Protocol (MCAP)
    # ATT = 0x001F  # See Bluetooth Core Specification
    THREEDSP = 0x0021  # See 3D Synchronisation Profile, Bluetooth SIG
    LE_PSM_IPSP = 0x0023  # See Internet Protocol Support Profile (IPSP), Bluetooth SIG
    OTS = 0x0025  # See Object Transfer Service (OTS), Bluetooth SIG

    L2CAP = 0x0100  # Bluetooth Core Specification


class ClassProfileIds:
    # Service class Profile Identifiers

    ServiceDiscoveryServerServiceClassID = 0x1000  # Bluetooth Core Specification	Service Class
    BrowseGroupDescriptorServiceClassID = 0x1001  # Bluetooth Core Specification	Service Class
    PublicBrowseGroup = 0x1002
    SerialPort = 0x1101  # Serial Port Profile (SPP) NOTE: The example SDP record in SPP v1.0 does not include a BluetoothProfileDescriptorList attribute, but some implementations may also use this UUID for the Profile Identifier.	Service Class/ Profile
    LANAccessUsingPPP = 0x1102  # LAN Access Profile [DEPRECATED] NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    DialupNetworking = 0x1103  # Dial-up Networking Profile (DUN) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    IrMCSync = 0x1104  # Synchronization Profile (SYNC) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    OBEXObjectPush = 0x1105  # Object Push Profile (OPP) NOTE: Used as both Service Class Identifier and Profile.	Service Class/ Profile
    OBEXFileTransfer = 0x1106  # File Transfer Profile (FTP) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    IrMCSyncCommand = 0x1107  # Synchronization Profile (SYNC)
    Headset = 0x1108  # Headset Profile (HSP) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    CordlessTelephony = 0x1109  # Cordless Telephony Profile (CTP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]	Service Class/ Profile
    AudioSource = 0x110A  # Advanced Audio Distribution Profile (A2DP)	Service Class
    AudioSink = 0x110B  # Advanced Audio Distribution Profile (A2DP)	Service Class
    AV_RemoteControlTarget = 0x110C  # Audio/Video Remote Control Profile (AVRCP)	Service Class
    AdvancedAudioDistribution = 0x110D  # Advanced Audio Distribution Profile (A2DP)	Profile
    AV_RemoteControl = 0x110E  # Audio/Video Remote Control Profile (AVRCP) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class/ Profile
    AV_RemoteControlController = 0x110F  # Audio/Video Remote Control Profile (AVRCP) NOTE: The AVRCP specification v1.3 and later require that 0x110E also be included in the ServiceClassIDList before 0x110F for backwards compatibility.	Service Class
    Intercom = 0x1110  # Intercom Profile (ICP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]	Service Class
    Fax = 0x1111  # Fax Profile (FAX) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]	Service Class
    Headset_Audio_Gateway_AG = 0x1112  # Headset Profile (HSP)	Service Class
    WAP = 0x1113  # Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]	Service Class
    WAP_CLIENT = 0x1114  # Interoperability Requirements for Bluetooth technology as a WAP, Bluetooth SIG [DEPRECATED]	Service Class
    PANU = 0x1115  # Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for PANU role.	Service Class / Profile
    NAP = 0x1116  # Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for NAP role.	Service Class / Profile
    GN = 0x1117  # Personal Area Networking Profile (PAN) NOTE: Used as both Service Class Identifier and Profile Identifier for GN role.	Service Class / Profile
    DirectPrinting = 0x1118  # Basic Printing Profile (BPP)	Service Class
    ReferencePrinting = 0x1119  # See Basic Printing Profile (BPP)	Service Class
    Basic_Imaging_Profile = 0x111A  # Basic Imaging Profile (BIP)	Profile
    ImagingResponder = 0x111B  # Basic Imaging Profile (BIP)	Service Class
    ImagingAutomaticArchive = 0x111C  # Basic Imaging Profile (BIP)	Service Class
    ImagingReferencedObjects = 0x111D  # Basic Imaging Profile (BIP)	Service Class
    Handsfree = 0x111E  # Hands-Free Profile (HFP) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class / Profile
    HandsfreeAudioGateway = 0x111F  # Hands-free Profile (HFP)	Service Class
    DirectPrintingReferenceObjectsService = 0x1120  # Basic Printing Profile (BPP)	Service Class
    ReflectedUI = 0x1121  # Basic Printing Profile (BPP)	Service Class
    BasicPrinting = 0x1122  # Basic Printing Profile (BPP)	Profile
    PrintingStatus = 0x1123  # Basic Printing Profile (BPP)	Service Class
    HumanInterfaceDeviceService = 0x1124  # Human Interface Device (HID) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class / Profile
    HardcopyCableReplacement = 0x1125  # Hardcopy Cable Replacement Profile (HCRP)	Profile
    HCR_Print = 0x1126  # Hardcopy Cable Replacement Profile (HCRP)	Service Class
    HCR_Scan = 0x1127  # Hardcopy Cable Replacement Profile (HCRP)	Service Class
    Common_ISDN_Access = 0x1128  # Common ISDN Access Profile (CIP) NOTE: Used as both Service Class Identifier and Profile Identifier. [DEPRECATED]	Service Class / Profile
    SIM_Access = 0x112D  # SIM Access Profile (SAP) NOTE: Used as both Service Class Identifier and Profile Identifier.	Service Class / Profile
    Phonebook_Access_PCE = 0x112E  # Phonebook Access Profile (PBAP)	Service Class
    Phonebook_Access_PSE = 0x112F  # Phonebook Access Profile (PBAP)	Service Class
    Phonebook_Access = 0x1130  # Phonebook Access Profile (PBAP)	Profile
    Headset_HS = 0x1131  # Headset Profile (HSP) NOTE: See erratum #3507.
    # 0x1108 and 0x1203 should also be included in the ServiceClassIDList before 0x1131 for backwards compatibility.	Service Class
    Message_Access_Server = 0x1132  # Message Access Profile (MAP)	Service Class
    Message_Notification_Server = 0x1133  # Message Access Profile (MAP)	Service Class
    Message_Access_Profile = 0x1134  # Message Access Profile (MAP)	Profile
    GNSS = 0x1135  # Global Navigation Satellite System Profile (GNSS)	Profile
    GNSS_Server = 0x1136  # Global Navigation Satellite System Profile (GNSS)	Service Class
    THREED_Display = 0x1137  # 3D Synchronisation Profile (3DSP) Service Class
    THREED_Glasses = 0x1138  # 3D Synchronization Profile (3DSP) Service Class
    THREED_Synchronization = 0x1139  # 3D Synchronization Profile (3DSP) Profile
    MPS_Profile_UUID = 0x113A  # Multi-Profile Specification (MPS)	Profile
    MPS_SC_UUID = 0x113B  # Multi-Profile Specification (MPS)	Service Class
    CTN_Access_Service = 0x113C  # Calendar, Task, and Notes (CTN) Profile Service Class
    CTN_Notification_Service = 0x113D  # Calendar Tasks and Notes (CTN) Profile Service Class
    CTN_Profile = 0x113E  # Calendar Tasks and Notes (CTN) Profile	Profile
    PnPInformation = 0x1200  # Device Identification (DID) NOTE: Used as both Service Class Identifier and Profile Identifier. Service Class / Profile
    GenericNetworking = 0x1201  # N/A	Service Class
    GenericFileTransfer = 0x1202  # N/A	Service Class
    GenericAudio = 0x1203  # N/A	Service Class
    GenericTelephony = 0x1204  # N/A	Service Class
    UPNP_Service = 0x1205  # Enhanced Service Discovery Profile (ESDP) [DEPRECATED]	Service Class
    UPNP_IP_Service = 0x1206  # Enhanced Service Discovery Profile (ESDP) [DEPRECATED]	Service Class
    ESDP_UPNP_IP_PAN = 0x1300  # Enhanced Service Discovery Profile (ESDP) [DEPRECATED]	Service Class
    ESDP_UPNP_IP_LAP = 0x1301  # Enhanced Service Discovery Profile (ESDP)[DEPRECATED]	Service Class
    ESDP_UPNP_L2CAP = 0x1302  # Enhanced Service Discovery Profile (ESDP)[DEPRECATED]	Service Class
    VideoSource = 0x1303  # Video Distribution Profile (VDP)	Service Class
    VideoSink = 0x1304  # Video Distribution Profile (VDP)	Service Class
    VideoDistribution = 0x1305  # Video Distribution Profile (VDP)	Profile
    HDP = 0x1400  # Health Device Profile	Profile
    HDP_Source = 0x1401  # Health Device Profile (HDP)	Service Class
    HDP_Sink = 0x1402  # Health Device Profile (HDP)	Service Class


class MinorDeviceClass:
    # Minor Device Class field - Peripheral Major Class

    NotKeyboardNotPointingDevice = 0x00
    Keyboard = 0x40
    PointingDevice = 0x80
    ComboKeyboardPointingDevice = 0xC0

    # Minor Class bits two to five for Peripheral Major Class

    UncategorizedDevice = 0x00
    Joystick = 0x04
    Gamepad = 0x08
    RemoteControl = 0x0C
    SensingDevice = 0x10
    DigitizerTablet = 0x14
    CardReader = 0x18
    DigitalPen = 0x1C
    HandheldScanner = 0x20
    HandheldGesturalInputDevice = 0x24


#######################################################################
# Attributes


class XMLElement:
    def xml(self, indent, xml):
        raise NotImplemented()

    @staticmethod
    def _indent(indent):
        # return " " * (indent * 4)
        return "\t" * indent


class Attribute(XMLElement):
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<attribute id=\"0x{:04x}\">\n".format(self.id)
        xml = self.content.xml(indent + 1, xml)
        xml += self._indent(indent) + "</attribute>\n"
        return xml


class Sequence(XMLElement):
    def __init__(self, *list):
        super(Sequence, self).__init__()
        self.list = list

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<sequence>\n"
        for element in self.list:
            xml = element.xml(indent + 1, xml)
        xml += self._indent(indent) + "</sequence>\n"
        return xml


class UUID(XMLElement):
    def __init__(self, value):
        super(UUID, self).__init__()
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<uuid value=\"0x{:04x}\" />\n".format(self.value)
        return xml


class UInt8(XMLElement):
    def __init__(self, value):
        super(UInt8, self).__init__()
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<uint8 value=\"0x{:02x}\" />\n".format(self.value)
        return xml


class UInt16(XMLElement):
    def __init__(self, value):
        super(UInt16, self).__init__()
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<uint16 value=\"0x{:04x}\" />\n".format(self.value)
        return xml


class UInt32(XMLElement):
    def __init__(self, value):
        super(UInt32, self).__init__()
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<uint16 value=\"0x{:08x}\" />\n".format(self.value)
        return xml


class Bool8(XMLElement):
    def __init__(self, value):
        super(Bool8, self).__init__()
        if not isinstance(value, bool):
            raise ValueError("Expected boolean but got " + str(type(value)))
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<boolean value=\"" + str(self.value).lower() + "\" />\n"
        return xml


class Text(XMLElement):
    def __init__(self, value, encoding=None):
        super(Text, self).__init__()
        self.value = value
        self.encoding = encoding

    def xml(self, indent, xml):
        if self.encoding is None:
            xml += self._indent(indent) + "<text value=\"" + self.value + "\" />\n"
        else:
            xml += self._indent(indent) + "<text encoding=\"" + self.encoding + "\" value=\"" + self.value + "\" />\n"
        return xml


class URL(XMLElement):
    def __init__(self, value):
        super(URL, self).__init__()
        self.value = value

    def xml(self, indent, xml):
        xml += self._indent(indent) + "<url value=\"" + self.value + "\" />\n"
        return xml


# Bluetooth Core Speficication: Universal Attributes

class ServiceRecordHandle(Attribute):
    def __init__(self, value):
        super(ServiceRecordHandle, self).__init__(0x0000, UInt32(value))


class ServiceClassIDList(Attribute):
    def __init__(self, *uuids):
        super(ServiceClassIDList, self).__init__(0x0001, Sequence(*[UUID(uuid) for uuid in uuids]))


class ServiceRecordState(Attribute):
    def __init__(self, value):
        super(ServiceRecordState, self).__init__(0x0002, UInt32(value))


class ServiceID(Attribute):
    def __init__(self, id):
        super(ServiceID, self).__init__(0x0003, UUID(id))


class ProtocolDescriptorList(Attribute):
    def __init__(self, *list):
        super(ProtocolDescriptorList, self).__init__(0x0004, Sequence(*list))


class BrowseGroupList(Attribute):
    def __init__(self, *list):
        super(BrowseGroupList, self).__init__(0x0005, Sequence(*list))


class LanguageBase:
    """
    Convenience type to define LanguageBase passed in LanguageBaseAttributeIDList attribute.
    """
    def __init__(self, iso_language_code, encoding, offset):
        """
        Constructor
        :param iso_language_code: as per ISO 639-1, two letter code from for instance https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        :param encoding: as per https://www.iana.org/assignments/character-sets/character-sets.xhtml - 106 (0x6A) - UTF-8 which is recommended
        :param offset: offset used for ServiceName, ServiceDescription and ProviderName attributes - examples ususally use 0x0100
        """
        self.iso_language_code = iso_language_code
        self.encoding = encoding  #
        self.offset = offset  #


class LanguageBaseAttributeIDList(Attribute):

    @staticmethod
    def uint16_from_iso_code(iso_code):
        if len(iso_code) != 2:
            raise ValueError("Expected two char iso code but got '" + iso_code + "'")
        return ord(iso_code[0]) * 256 + ord(iso_code[1])

    @staticmethod
    def flatmap(elements):
        return reduce(lambda arr1, arr2: arr1 + arr2, elements)

    def __init__(self, *language_bases):
        for language_base in language_bases:
            if not isinstance(language_base, LanguageBase):
                raise ValueError("Only arguments of LanguageBase are accepted; got " + str(type(language_base)))
        super(LanguageBaseAttributeIDList, self).__init__(0x0006, Sequence(*LanguageBaseAttributeIDList.flatmap([[UInt16(LanguageBaseAttributeIDList.uint16_from_iso_code(lb.iso_language_code)), UInt16(lb.encoding), UInt16(lb.offset)] for lb in language_bases])))


class ServiceInfoTimeToLive(Attribute):
    def __init__(self, value):
        super(ServiceInfoTimeToLive, self).__init__(0x0007, UInt32(value))


class ServiceAvailability(Attribute):
    def __init__(self, value):
        super(ServiceAvailability, self).__init__(0x0008, UInt8(value))


class BluetoothProfileDescriptorList(Attribute):
    def __init__(self, *list):
        super(BluetoothProfileDescriptorList, self).__init__(0x0009, Sequence(*list))


class DocumentationURL(Attribute):
    def __init__(self, url):
        super(DocumentationURL, self).__init__(0x000A, URL(url))


class ClientExecutableURL(Attribute):
    def __init__(self, url):
        super(ClientExecutableURL, self).__init__(0x000B, URL(url))


class IconURL(Attribute):
    def __init__(self, url):
        super(IconURL, self).__init__(0x000C, URL(url))


class AdditionalProtocolDescriptorLists(Attribute):
    def __init__(self, *list):
        super(AdditionalProtocolDescriptorLists, self).__init__(0x000D, Sequence(*list))


class ServiceName(Attribute):
    def __init__(self, offset, name):
        super(ServiceName, self).__init__(offset + 0x0000, Text(name))


class ServiceDescription(Attribute):
    def __init__(self, offset, desc):
        super(ServiceDescription, self).__init__(offset + 0x0001, Text(desc))


class ProviderName(Attribute):
    def __init__(self, offset, name):
        super(ProviderName, self).__init__(offset + 0x0002, Text(name))


# Bluetooth HID

class HIDDeviceReleaseNumber(Attribute):  # Deprecated
    def __init__(self, value):
        super(HIDDeviceReleaseNumber, self).__init__(0x0200, UInt16(value))


class HIDProfileVersion(Attribute):
    def __init__(self, value):
        super(HIDProfileVersion, self).__init__(0x0201, UInt16(value))


class HIDDeviceSubclass(Attribute):
    def __init__(self, value):
        super(HIDDeviceSubclass, self).__init__(0x0202, UInt8(value))


class HIDCountryCode(Attribute):
    def __init__(self, value):
        super(HIDCountryCode, self).__init__(0x0203, UInt8(value))


class HIDVirtualCable(Attribute):
    def __init__(self, value):
        super(HIDVirtualCable, self).__init__(0x0204, Bool8(value))


class HIDReconnectInitiate(Attribute):
    def __init__(self, value):
        super(HIDReconnectInitiate, self).__init__(0x0205, Bool8(value))


class HIDDescriptorList(Attribute):
    Report = 0x22
    PhysicalDescriptor = 0x23

    def __init__(self, report=None, physical_descriptor=None, encoding="hex"):
        super(HIDDescriptorList, self).__init__(0x0206, None)
        if (report is None and physical_descriptor is None) or (report is not None and physical_descriptor is not None):
            raise ValueError("You need to supply at least and only one of 'report' or 'physical_descriptor' parameter")
        if report is not None:
            self.kind = self.Report
            self.content = Sequence(Sequence(UInt8(self.kind), Text(report, encoding=encoding)))
        else:
            self.kind = self.PhysicalDescriptor
            self.content = Sequence(Sequence(UInt8(self.kind), Text(physical_descriptor, encoding=encoding)))


class HIDLANGIDBase:
    """
    http://info.linuxoid.in/datasheets/USB%202.0a/USB_LANGIDs.pdf
    """
    def __init__(self, language_id, base_attribute_id):
        """

        :param language_id: as per http://info.linuxoid.in/datasheets/USB%202.0a/USB_LANGIDs.pdf 0x0409 is English (United States)
        :param base_attribute_id: offset used for ServiceName, ServiceDescription and ProviderName attributes - examples ususally use 0x0100
        """
        self.language_id = language_id
        self.base_attribute_id = base_attribute_id


class HIDLANGIDBaseList(Attribute):
    def __init__(self, *hid_lang_id_bases):
        for hid_lang_id_base in hid_lang_id_bases:
            if not isinstance(hid_lang_id_base, HIDLANGIDBase):
                raise ValueError("Only arguments of HIDLANGIDBase are accepted; got " + str(type(hid_lang_id_base)))

        super(HIDLANGIDBaseList, self).__init__(0x0207, Sequence(*[Sequence(UInt16(hlid.language_id), UInt16(hlid.base_attribute_id)) for hlid in hid_lang_id_bases]))


class HIDSDPDisable(Attribute):
    def __init__(self, value):
        super(HIDSDPDisable, self).__init__(0x0208, Bool8(value))


class HIDBatteryPower(Attribute):
    def __init__(self, value):
        super(HIDBatteryPower, self).__init__(0x0209, Bool8(value))


class HIDRemoteWake(Attribute):
    def __init__(self, value):
        super(HIDRemoteWake, self).__init__(0x020A, Bool8(value))


class HIDParserVersion(Attribute):
    def __init__(self, value):
        super(HIDParserVersion, self).__init__(0x020B, UInt16(value))


class HIDSupervisionTimeout(Attribute):
    def __init__(self, value):
        super(HIDSupervisionTimeout, self).__init__(0x020C, UInt16(value))


class HIDNormallyConnectable(Attribute):
    def __init__(self, value):
        super(HIDNormallyConnectable, self).__init__(0x020D, Bool8(value))


class HIDBootDevice(Attribute):
    def __init__(self, value):
        super(HIDBootDevice, self).__init__(0x020E, Bool8(value))


class HIDSSRHostMaxLatency(Attribute):
    def __init__(self, value):
        super(HIDSSRHostMaxLatency, self).__init__(0x020F, UInt16(value))


class HIDSSRHostMinTimeout(Attribute):
    def __init__(self, value):
        super(HIDSSRHostMinTimeout, self).__init__(0x0210, UInt16(value))


class SDPRecord:
    MANDATORY_ATTRIBUTES = [
        HIDBootDevice, HIDCountryCode, HIDDescriptorList, HIDDeviceSubclass,
        HIDLANGIDBaseList, HIDParserVersion, HIDProfileVersion, HIDReconnectInitiate,
        HIDVirtualCable,
    ]

    def __init__(self):
        self.attributes = []

    def __add__(self, other):
        if not isinstance(other, Attribute):
            raise ValueError("Expected attribute but got " + str(type(other)))
        self.attributes.append(other)
        self.attributes = sorted(self.attributes, key=lambda a: a.id)
        return self

    def add(self, other):
        return self.__add__(other)

    def xml(self):
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n\n<record>\n"
        for attribute in self.attributes:
            xml = attribute.xml(1, xml)

        xml += "</record>\n"
        return xml


def create_simple_HID_SDP_Report(service_name, service_description, provider_name, hid_report_descriptor,
                                 subclass=MinorDeviceClass.Gamepad,
                                 normally_connectable=True, virtual_cable=False, reconnect_reinitiate=False, boot_device=False):
    record = SDPRecord()
    record += ServiceClassIDList(ClassProfileIds.HumanInterfaceDeviceService)
    record += ProtocolDescriptorList(Sequence(UUID(Consts.L2CAP), UInt16(Consts.HIDP)), Sequence(UUID(Consts.HIDP)))
    record += BrowseGroupList(UUID(ClassProfileIds.PublicBrowseGroup))
    record += LanguageBaseAttributeIDList(
        LanguageBase('en', 0x006a, 0x0100))  # 'en' (0x656e), 0x006A is UTF-8 encoding, 0x0100 represents attribute ID offset used for ServiceName, ServiceDescriptor and ProviderName attributes!
    record += BluetoothProfileDescriptorList(Sequence(UUID(ClassProfileIds.HumanInterfaceDeviceService), UInt16(0x0100)))  # 0x0100 indicating version 1.0
    record += AdditionalProtocolDescriptorLists(Sequence(Sequence(UUID(Consts.L2CAP), UInt16(Consts.HID_Interrupt)), Sequence(UUID(Consts.HIDP))))
    record += ServiceName(0x0100, service_name)  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
    record += ServiceDescription(0x0100, service_description)  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
    record += ProviderName(0x0100, provider_name)  # 0x0100 is offset from LanguageBaseAttributeIDList for 'en' language (0x656e)
    record += HIDDeviceReleaseNumber(0x100)  # deprecated release number 1.0
    record += HIDProfileVersion(0x0111)  # indicating version 1.11
    record += HIDDeviceSubclass(subclass)
    record += HIDCountryCode(0x00)
    record += HIDVirtualCable(virtual_cable)
    record += HIDReconnectInitiate(reconnect_reinitiate)
    record += HIDLANGIDBaseList(HIDLANGIDBase(0x0409, 0x0100))  # 0x0409 per http://info.linuxoid.in/datasheets/USB%202.0a/USB_LANGIDs.pdf is English (United States)
    record += HIDDescriptorList(report=hid_report_descriptor.hex().lower(), encoding="hex")
    record += HIDParserVersion(0x0100)  # 1.0
    record += HIDSupervisionTimeout(0x0c80)  # 3200
    record += HIDNormallyConnectable(normally_connectable)
    record += HIDBootDevice(boot_device)
    record += HIDSSRHostMaxLatency(0x0640)  # 1600
    record += HIDSSRHostMinTimeout(0x0320)  # 800

    return record


if __name__ == "__main__":

    # Testing creation of SDPRecord

    import hid_report_descriptor
    from hid_report_descriptor import Usage

    hid_descriptor = hid_report_descriptor.create_joystick_report_descriptor(kind=Usage.Gamepad,
                                                                             axes=(Usage.X, Usage.Y, Usage.Rx, Usage.Ry),
                                                                             button_number=14)

    record = create_simple_HID_SDP_Report("A Virtual Gamepad Controller", "Keyboard > BT Gamepad", "GCC",
                                          hid_descriptor,
                                          subclass=MinorDeviceClass.Gamepad)

    print("Record=\n" + record.xml())
