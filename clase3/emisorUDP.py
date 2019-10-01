import socket
import struct
import sys
from TCPPackets import *

def stop_and_wait(connection,my_socket,data):
    try:
        connection.send(data)
        response,addr =my_socket.recvfrom(64)
        return response
    except socket.timeout:
        return stop_and_wait(connection,my_socket,data)
# Tamaño de los paquetes son de 64 bits
def handshake(my_socket,conn):
    syn = createSyn('')
    stop_and_wait(conn,my_socket,syn)
    ack = createAck('')
    stop_and_wait(conn,my_socket,ack)
# 
def conexion_end(connection):
    pass

# crea par numero de secuencia + trozo de mensaje en el receptor
def split_message(message:str)->list():
    return list()
# stados -> esperar un ack, enviando un paquete.
# 
def run(message: str) -> int:
    host = "127.0.0.1"
    udp_port = 3000
    my_port = 3001
    server = (host,my_port)
    my_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    my_server.settimeout(10.0)
    my_server.bind((host,my_port))
    while True:
        receiver = (host,udp_port)
        packet = createPacket(0,0,0,message)
        print(packet)
        connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        handshake(my_server,connection)
        stop_and_wait(connection,my_server,message)
        conexion_end(connection)
    return 0
if __name__ == "__main__":
    message = sys.argv[1]
    run(message)