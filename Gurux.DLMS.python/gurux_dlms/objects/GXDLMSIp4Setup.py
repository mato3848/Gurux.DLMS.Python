#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import socket
import struct
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from .GXDLMSIp4SetupIpOption import GXDLMSIp4SetupIpOption
from .enums.Ip4SetupIpOptionType import Ip4SetupIpOptionType

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSIp4Setup
#
# pylint: disable=too-many-instance-attributes
class GXDLMSIp4Setup(GXDLMSObject, IGXDLMSBase):
    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln="0.0.25.1.0.255", sn=0):
        super(GXDLMSIp4Setup, self).__init__(ObjectType.IP4_SETUP, ln, sn)
        self.dataLinkLayerReference = None
        self.ipAddress = None
        self.multicastIPAddress = list()
        self.ipOptions = list()
        self.subnetMask = None
        self.gatewayIPAddress = None
        self.useDHCP = False
        self.primaryDNSAddress = None
        self.secondaryDNSAddress = None

    def getValues(self):
        return [self.logicalName,
                self.dataLinkLayerReference,
                self.ipAddress,
                self.multicastIPAddress,
                self.ipOptions,
                self.subnetMask,
                self.gatewayIPAddress,
                self.useDHCP,
                self.primaryDNSAddress,
                self.secondaryDNSAddress]

    #
    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  DataLinkLayerReference
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  IPAddress
        if all_ or self.canRead(3):
            attributes.append(3)
        #  MulticastIPAddress
        if all_ or self.canRead(4):
            attributes.append(4)
        #  IPOptions
        if all_ or self.canRead(5):
            attributes.append(5)
        #  SubnetMask
        if all_ or self.canRead(6):
            attributes.append(6)
        #  GatewayIPAddress
        if all_ or self.canRead(7):
            attributes.append(7)
        #  UseDHCP
        if all_ or not self.isRead(8):
            attributes.append(8)
        #  PrimaryDNSAddress
        if all_ or self.canRead(9):
            attributes.append(9)
        #  SecondaryDNSAddress
        if all_ or self.canRead(10):
            attributes.append(10)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 10

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 3

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.OCTET_STRING
        elif index == 3:
            ret = DataType.UINT32
        elif index == 4:
            ret = DataType.ARRAY
        elif index == 5:
            ret = DataType.ARRAY
        elif index == 6:
            ret = DataType.UINT32
        elif index == 7:
            ret = DataType.UINT32
        elif index == 8:
            ret = DataType.BOOLEAN
        elif index == 9:
            ret = DataType.UINT32
        elif index == 10:
            ret = DataType.UINT32
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = _GXCommon.logicalNameToBytes(self.dataLinkLayerReference)
        elif e.index == 3:
            ret = struct.unpack("!I", socket.inet_aton(self.ipAddress))[0]
        elif e.index == 4:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY.value)
            if not self.multicastIPAddress:
                _GXCommon.setObjectCount(0, data)
            else:
                _GXCommon.setObjectCount(len(self.multicastIPAddress), data)
                for it in self.multicastIPAddress:
                    _GXCommon.setData(data, DataType.UINT16, it)
            ret = data
        elif e.index == 5:
            data = GXByteBuffer()
            data.setUInt8(DataType.ARRAY.value)
            if not self.ipOptions:
                data.setUInt8(0)
            else:
                _GXCommon.setObjectCount(len(self.ipOptions), data)
                for it in self.ipOptions:
                    data.setUInt8(DataType.STRUCTURE.value)
                    data.setUInt8(3)
                    _GXCommon.setData(data, DataType.UINT8, it.type_)
                    _GXCommon.setData(data, DataType.UINT8, it.length)
                    _GXCommon.setData(data, DataType.OCTET_STRING, it.data)
            ret = data.array()
        elif e.index == 6:
            ret = struct.unpack("!I", socket.inet_aton(self.subnetMask))[0]
        elif e.index == 7:
            ret = struct.unpack("!I", socket.inet_aton(self.gatewayIPAddress))[0]
        elif e.index == 8:
            ret = self.useDHCP
        elif e.index == 9:
            ret = struct.unpack("!I", socket.inet_aton(self.primaryDNSAddress))[0]
        elif e.index == 10:
            ret = struct.unpack("!I", socket.inet_aton(self.secondaryDNSAddress))[0]
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            if isinstance(e.value, str):
                self.dataLinkLayerReference = e.value
            else:
                self.dataLinkLayerReference = _GXCommon.toLogicalName(e.value)
        elif e.index == 3:
            self.ipAddress = socket.inet_ntoa(struct.pack("!I", e.value))
        elif e.index == 4:
            self.multicastIPAddress.clear()
            if e.value:
                for it in e.value:
                    self.multicastIPAddress.append(socket.inet_ntoa(struct.pack("!I", it)))
        elif e.index == 5:
            self.ipOptions.clear()
            if e.value:
                for it in e.value:
                    item = GXDLMSIp4SetupIpOption()
                    item.type_ = Ip4SetupIpOptionType(it[0])
                    item.length = it[1]
                    item.data = it[2]
                    self.ipOptions.append(item)
        elif e.index == 6:
            self.subnetMask = socket.inet_ntoa(struct.pack("!I", e.value))
        elif e.index == 7:
            self.gatewayIPAddress = socket.inet_ntoa(struct.pack("!I", e.value))
        elif e.index == 8:
            self.useDHCP = e.value
        elif e.index == 9:
            self.primaryDNSAddress = socket.inet_ntoa(struct.pack("!I", e.value))
        elif e.index == 10:
            self.secondaryDNSAddress = socket.inet_ntoa(struct.pack("!I", e.value))
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.dataLinkLayerReference = reader.readElementContentAsString("DataLinkLayerReference")
        self.ipAddress = reader.readElementContentAsString("IPAddress")
        self.multicastIPAddress.clear()
        if reader.isStartElement("MulticastIPAddress", True):
            while reader.isStartElement("Value", False):
                self.multicastIPAddress.append(reader.readElementContentAsInt("Value"))
            reader.readEndElement("MulticastIPAddress")
        self.ipOptions.clear()
        if reader.isStartElement("IPOptions", True):
            while reader.isStartElement("IPOptions", True):
                it = GXDLMSIp4SetupIpOption()
                it.type = Ip4SetupIpOptionType(reader.readElementContentAsInt("Type"))
                it.length = reader.readElementContentAsInt("Length")
                it.data = GXByteBuffer.hexToBytes(reader.readElementContentAsString("Data"))
                self.ipOptions.append(it)
            reader.readEndElement("IPOptions")
        self.subnetMask = reader.readElementContentAsString("SubnetMask")
        self.gatewayIPAddress = reader.readElementContentAsString("GatewayIPAddress")
        self.useDHCP = reader.readElementContentAsInt("UseDHCP") != 0
        self.primaryDNSAddress = reader.readElementContentAsString("PrimaryDNSAddress")
        self.secondaryDNSAddress = reader.readElementContentAsString("SecondaryDNSAddress")

    def save(self, writer):
        writer.writeElementString("DataLinkLayerReference", self.dataLinkLayerReference)
        writer.writeElementString("IPAddress", self.ipAddress)
        if self.multicastIPAddress:
            writer.writeStartElement("MulticastIPAddress")
            for it in self.multicastIPAddress:
                writer.writeElementString("Value", it)
            writer.writeEndElement()
        if self.ipOptions:
            writer.writeStartElement("IPOptions")
            for it in self.ipOptions:
                writer.writeStartElement("IPOptions")
                writer.writeElementString("Type", it.type_)
                writer.writeElementString("Length", it.length)
                writer.writeElementString("Data", GXByteBuffer.hex(it.data))
                writer.writeEndElement()
            writer.writeEndElement()
        writer.writeElementString("SubnetMask", self.subnetMask)
        writer.writeElementString("GatewayIPAddress", self.gatewayIPAddress)
        writer.writeElementString("UseDHCP", self.useDHCP)
        writer.writeElementString("PrimaryDNSAddress", self.primaryDNSAddress)
        writer.writeElementString("SecondaryDNSAddress", self.secondaryDNSAddress)