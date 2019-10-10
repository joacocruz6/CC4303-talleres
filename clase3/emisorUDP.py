import socket
import struct
import sys
import signal
from TCPPackets import *

def stop_and_wait(my_socket,data,receiver):
    my_socket.sendto(data,receiver)
    while True:
        try:
            response,addr = my_socket.recvfrom(64)
            return PacketFactory.parseBytes(response)
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
def alarmHandler():
    pass
signal.signal(signal.SIGALRM,alarmHandler)
# 
def conexion_end(my_socket,receiver):
    fin = PacketFactory.createFin('',0,0)
    response_fin = stop_and_wait(my_socket,fin.generatePacket(),receiver)
    while True:
        try:
            data,addr = my_socket.recvfrom(64)
            data = PacketFactory.parseBytes(data)
            if data.fin == 1:
                my_socket.sendto(UDPPacket(1,data.sqn,0,1,0,''),receiver)
                signal.alarm(30)
        except socket.timeout:
            continue

def partData(msg: str)->list():
    return ([msg],1)
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
    buffer,N = partData(message)
    lizq = 0
    lder = N
    while True:
        receiver = (host,udp_port)
        handshake(my_server,(host,udp_port))
        packet = UDPPacket(100,0,0,1,0,message)
        stop_and_wait(my_server,packet.generatePacket(),receiver)
        conexion_end(my_server,receiver)
    return 0
if __name__ == "__main__":
    message = sys.argv[1]
    run(message)