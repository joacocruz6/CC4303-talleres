from packetesIP import *
import socket
import sys
from collections import namedtuple
def main(args:list)->int:
    host = args[1]
    port = args[2]
    table = args[3]
    my_address = (host,int(port))
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_socket.bind(my_address)
    DATA_SIZE = 16 * 1024
    tablas_ruteo = namedtuple("tabla","red puerto_inicial puerto_final ip_llegada puerto_llegada")
    tabla_ruteo = RouteParser.makeRouteTable(table,tablas_ruteo)
    while True:
        data_received,addr = my_socket.recvfrom(DATA_SIZE)
        if data_received:
            ip_packet = PacketParser.makePacketFromData(data_received)
            if ip_packet.getDestFinal() == host and ip_packet.getPortFinal() == port:
                print(ip_packet.data)

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