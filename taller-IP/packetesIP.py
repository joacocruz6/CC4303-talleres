import struct
from collections import namedtuple
class PacketIP(object):
    def __init__(self,data: str,ip_src:str,ip_dest: str,ip_dest_final: str,port_dest_f: str):
        self.data = data
        self.header = list()
        self.header.append(ip_dest_final)
        self.header.append(port_dest_f)
    def codeHeader(self)->bytes:
        my_header = ";".join(self.header)
        return bytes(my_header,"utf-8")
    def codeData(self):
        return bytes(self.data,"utf-8")
    def createPacket(self):
        return self.codeHeader() + "#"+ self.codeData()
    def decodePacket(self,data):
        data = data.split(b"#")
        my_header = data[0]
        my_data = data[1]
        self.header = list(map(lambda x: x.decode("utf-8"),my_header.split(b";")))
        self.data = my_data.decode("utf-8")
    def getDestFinal(self):
        return self.header[0]
    def getPortFinal(self):
        return self.header[1]
    def __repr__(self):
        return f"ip_dest_final:{self.header[0]}\nport_destino_final:{self.header[1]}\ndata:{self.data}"
class PacketParser(object):
    @staticmethod
    def makePacketFromData(data:bytes)->PacketIP:
        my_packet = PacketIP("","","","","")
        my_packet.decodePacket(data)
        return my_packet
class RouteParser(object):
    @staticmethod
    def makeRouteTable(file_name:str,constructor)->list:
        table = list()
        with open(file_name,"r") as my_file:
            for line in my_file:
                line = line[:-1]
                line = line.split(',')
                obj = constructor(line[0],line[1],line[2],line[3],line[4])
                table.append(obj)
        return table