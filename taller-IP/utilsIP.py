import struct
from collections import namedtuple
class Route(object):
    @staticmethod
    def compare(network:str,bits:int,ip:str)->bool:
        network = network.split('.')
        ip = ip.split('.')
        i = 0
        while i<bits:
            if network[i] != ip[i]:
                return False
            i+=1
        return True
    def __init__(self,red: str, bits: str,puerto_inicial: str, puerto_final: str, ip_llegada: str, puerto_llegada: str):
        self.red = red
        self.bits = int(bits) // 8
        self.puerto_inicial = int(puerto_inicial)
        self.puerto_final = int(puerto_final)
        self.ip_llegada = ip_llegada
        self.puerto_llegada = int(puerto_llegada)
    def __repr__(self):
        return f"Route(red={self.red},bits={self.bits},init_port={self.puerto_inicial},fin_port={self.puerto_final},dest_ip={self.ip_llegada},dest_port={self.puerto_llegada})"
    def getIp_llegada(self)->str:
        return self.ip_llegada
    def getPuertollegada(self)->int:
        return self.puerto_llegada
    def canForward(self,ip:str,port:str)->bool:
        port = int(port)
        return Route.compare(self.red,self.bits,ip) and self.puerto_inicial <= port <= self.puerto_final
    

class PacketIP(object):
    def __init__(self,data: str,ip_src:str,ip_dest: str,ip_dest_final: str,port_dest_f: str,ttl: str):
        self.data = data
        self.header = list()
        self.header.append(ip_dest_final)
        self.header.append(port_dest_f)
        self.header.append(int(ttl))
    def codeHeader(self)->bytes:
        my_header = list(map(lambda x: str(x),self.header))
        my_header = ";".join(my_header)
        return bytes(my_header,"utf-8")
    def codeData(self):
        return bytes(self.data,"utf-8")
    def createPacket(self):
        return self.codeHeader() + b"#"+ self.codeData()
    def decodePacket(self,data):
        data = data.split(b"#")
        my_header = data[0]
        my_data = data[1]
        self.header = list(map(lambda x: x.decode("utf-8"),my_header.split(b";")))
        self.header[2] = int(self.header[2])
        self.data = my_data.decode("utf-8")
    def __len__(self):
        return len(bytes(self.data,"utf-8"))
    def getDestFinal(self):
        return self.header[0]
    def getPortFinal(self):
        return self.header[1]
    def getTTL(self):
        return self.header[2]
    def setTTL(self,new_ttl: int):
        self.header[2] = new_ttl
    def minusTTL(self):
        self.header[2] = self.header[2]-1
    def __repr__(self):
        return f"ip_dest_final:{self.header[0]}\nport_destino_final:{self.header[1]}\ndata:{self.data}"
class PacketParser(object):
    @staticmethod
    def makePacketFromData(data:bytes)->PacketIP:
        my_packet = PacketIP("","","","","","0")
        my_packet.decodePacket(data)
        return my_packet
class RouteParser(object):
    @staticmethod
    def makeRouteTable(file_name:str)->list:
        table = list()
        with open(file_name,"r") as my_file:
            for line in my_file:
                line = line[:-1]
                line = line.split(',')
                red = line[0].split('/')
                obj = Route(red[0],red[1],line[1],line[2],line[3],line[4])
                table.append(obj)
        return table