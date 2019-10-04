import socket
import struct
import sys
from TCPPackets import *

def stop_and_wait(my_socket,data,receiver):
    my_socket.sendto(data,receiver)
    while True:
        try:
            response,addr = my_socket.recvfrom(64)
            return PacketFactory.createDecodedPacket(response)
        except socket.timeout:
            print("timeout!")
            my_socket.sendto(data,receiver)
# Tamaño de los paquetes son de 64 bits
def handshake(my_socket,receiver):
    syn = PacketFactory.createSyn('',0)
    while True:
        response_syn=stop_and_wait(my_socket,syn,receiver)
        if response_syn.syn == 1:
            return
# 
def conexion_end(my_socket,receiver):
    fin = PacketFactory.createFin('',0,0)
    response_fin = stop_and_wait(my_socket,fin.generatePacket(),receiver)
    data,addr = my_socket.recvfrom(64)
    

# stados -> esperar un ack, enviando un paquete.
# 
def run(message: str) -> int:
    host = "127.0.0.1"
    udp_port = 3000
    my_port = 3001
    server = (host,my_port)
    my_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_server.settimeout(5.0)
    my_server.bind((host,my_port))
    while True:
        receiver = (host,udp_port)
        handshake(my_server,(host,udp_port),)
        packet = UDPPacket(100,0,0,1,0,message)
        stop_and_wait(my_server,packet.generatePacket(),receiver)
        conexion_end(my_server,receiver)
    return 0
if __name__ == "__main__":
    message = sys.argv[1]
    run(message)