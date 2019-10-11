from utilsIP import *
import socket
import sys
from collections import namedtuple
MAX_INT = 2**30
NULL = None
def tableLookup(table: list,ip:str,port: str)->tuple:
    # uses round robin to the lookup
    candidate = NULL
    min_carga = MAX_INT
    for route in table:
        if route.canForward(ip,port) and route.getCarga() < min_carga:
            candidate = route
            min_carga = route.getCarga()
    if candidate == NULL:
        raise Exception('No routes')
    candidate.addCarga()
    return (candidate.getIp_llegada(),candidate.getPuertollegada())
def main(args:list)->int:
    host = args[1]
    port = args[2]
    table = args[3]
    my_address = (host,int(port))
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_socket.bind(my_address)
    DATA_SIZE = 16 * 1024
    tabla_ruteo = RouteParser.makeRouteTable(table)
    while True:
        data_received,addr = my_socket.recvfrom(DATA_SIZE)
        if data_received:
            ip_packet = PacketParser.makePacketFromData(data_received)
            if ip_packet.getDestFinal() == host and ip_packet.getPortFinal() == port:
                print(ip_packet.data)
            else:
                next_destination = tableLookup(tabla_ruteo,ip_packet.getDestFinal(),ip_packet.getPortFinal())
                fast_forwarding = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                fast_forwarding.sendto(ip_packet.createPacket(),next_destination)
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