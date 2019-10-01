import socket
import struct
from TCPPackets import *
def run()-> int:
    port = 3000
    host = "127.0.0.1"
    emitter = 3001
    my_app = (host,port)
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connection.bind(my_app) 
    while True:
        data,addr = connection.recvfrom(64)
        packet = decodePacket(data)
        print(packet)
        packet_response = createPacket(0,1,0,"")
        connection.sendto(packet_response,(host,emitter))
    return 0
if __name__ == "__main__":
    run()