import struct
class UDPPacket(object):
    def __init__(self,sqn:int,ackn:int,syn:int,ack:int,fin:int,data:str):
        self.sqn = sqn
        self.ackn = ack
        self.syn = syn
        self.ack = ack
        self.fin = fin
        self.data = data
        self.header = 0
        self.bytes_data = b''
    def createHeader(self):
        self.header = 0
        self.header |= self.sqn
        self.header <<= 16
        self.header |= self.ackn
        self.header <<= 1
        self.header |= self.syn
        self.header <<= 1
        self.header |= self.ack
        self.header <<= 1
        self.header |= self.fin
        print(self.header)
    def createData(self):
        self.bytes_data = bytes("#"+self.data,"utf-8")
    def generatePacket(self)->bytes:
        packet = b''
        self.createHeader()
        self.createData()
        packet += struct.pack(">Q",self.header)
        packet += self.bytes_data
        return packet
    def decodeHeader(self):
        self.fin = self.header & 1
        self.header >>= 1
        self.ack = self.header & 1
        self.header >>= 1
        self.syn = self.header & 1
        self.header >>= 1
        self.ackn = self.header & 0xffff
        self.header >>= 16
        self.sqn = self.header & 0xffff
    def decodePacket(self,data_received):
        data_received = data_received.split(b"#")
        data_header = data_received[0]
        data_packet = data_received[1]
        self.header = struct.unpack(">Q",data_header)[0]
        self.decodeHeader()
        self.data = data_packet
    def __repr__(self)->str:
        return f"sqn:{self.sqn}\nackn:{self.ackn}\nsyn:{self.syn}\nack:{self.ack}\nfin:{self.fin}\ndata:{self.data}"
class PacketFactory(object):
    @staticmethod
    def createSyn(data:str,sqn:int)->UDPPacket:
        pack = UDPPacket(sqn,0,1,0,0,data)
        data = pack.generatePacket()
        return data
    @staticmethod
    def createAck(data:str,sqn:int,ackn:int,syn=0)->UDPPacket:
        pack = UDPPacket(sqn,ackn,syn,1,0,data)
        data = pack.generatePacket()
        return data
    @staticmethod
    def createFin(data:str,sqn:int,ackn:int,ack=0)->UDPPacket:
        pack = UDPPacket(sqn,ackn,0,ack,1,data)
        data = pack.generatePacket()
        return data
    @staticmethod
    def parseBytes(data:bytes):
        pack = UDPPacket(0,0,0,0,0,data)
        pack.decodePacket(data)
        return pack