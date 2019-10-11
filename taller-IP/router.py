from packetesIP import *
import socket
import sys
from collections import namedtuple
def compare(network:str,bits: str,ip:str)->bool:
    bits = int(bits)
    number_bytes = bits // 8
    network = network.split('.')
    ip = ip.split('.')
    i = 0
    while i < number_bytes:
        if network[i] != ip[i]:
            return False
        i+=1
    return True
def tableLookup(table: list,ip:str,port: str)->tuple:
    pass
def main(args:list)->int:
    host = args[1]
    port = args[2]
    table = args[3]
    my_address = (host,int(port))
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_socket.bind(my_address)
    DATA_SIZE = 16 * 1024
    tablas_ruteo = namedtuple("tabla","red bits puerto_inicial puerto_final ip_llegada puerto_llegada")
    tabla_ruteo = RouteParser.makeRouteTable(table,tablas_ruteo)
    while True:
        data_received,addr = my_socket.recvfrom(DATA_SIZE)
        if data_received:
            ip_packet = PacketParser.makePacketFromData(data_received)
            if ip_packet.getDestFinal() == host and ip_packet.getPortFinal() == port:
                print(ip_packet.data)
            else:
                
if __name__ == "__main__":
    main(sys.argv)
## nc -u ip_router port_rocuter < archivo <<EOF
"""
Archivo puede ser del estilo:
Hola
Soy
Un ejemplo
EOF
"""