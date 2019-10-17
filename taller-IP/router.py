from utilsIP import *
import socket
import sys
from collections import namedtuple
MAX_INT = 2**30
NULL = None
def tableLookup(table: list,ip:str,port: str)->tuple:
    # uses round robin to the lookup
    candidate = NULL
    for route in table:
        if route.canForward(ip,port):
            candidate = route
            break
    if candidate == NULL:
        raise Exception('No routes')
    ## Round Robin to the candidate found, put it on the bottom of the list
    table.remove(candidate)
    table.append(candidate)
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
    MTU = [{
        'src': 8881,
        'dest' : 8882,
        'MTU' : 300
    },
    {
        'src': 8882,
        'dest' : 8883,
        'MTU' : 300
    },
    {
        'src': 8883,
        'dest' : 8884,
        'MTU' : 100
    },
    {
        'src': 8884,
        'dest' : 8885,
        'MTU' : 200
    },
    {
        'src': 8883,
        'dest' : 8885,
        'MTU' : 300
    },
    ]
    while True:
        data_received,addr = my_socket.recvfrom(DATA_SIZE)
        if data_received:
            ip_packet = PacketParser.makePacketFromData(data_received)
            ip_packet.minusTTL()
            if ip_packet.getTTL() != 0:    
                if ip_packet.getDestFinal() == host and ip_packet.getPortFinal() == port:
                    print(ip_packet.data)
                else:
                    print(len(ip_packet))
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