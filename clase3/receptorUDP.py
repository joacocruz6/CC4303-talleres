import socket
import struct
import random
from TCPPackets import *
def accept_handshake(receiver,first_seqn):
    while True:
        try:
            data_syn,addr = receiver.recvfrom(64)
            data_syn = PacketFactory.parseBytes(data_syn)
            if data_syn != 1:
                continue
            data_syn_ack = PacketFactory.createAck('',first_seqn,data_syn.ackn,1)
            receiver.sendto(data_syn_ack.generatePacket(),addr)
            while True:
                try:
                    segment,addr = receiver.recvfrom(64)
                    segment = PacketFactory.parseBytes(segment)
                    
                except socket.timeout:
                    receiver.sendto(data_syn_ack.generatePacket(),addr)
        except socket.timeout:
            continue
def end_connection(receiver_socket,emitter):
    pass
def run()-> int:
    port = 3000
    host = "127.0.0.1"
    my_app = (host,port)
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connection.timeout(5.0)
    connection.bind(my_app)
    first_sqn = random.randint(0,65535//2)
    while True:
        (addr,seqn,first_segment) = accept_handshake(connection,first_sqn)
        first_segment_ack = PacketFactory.createAck('',seqn+1,first_segment.seqn)
        connection.sendto(first_segment_ack.generatePacket(),addr)
        while True:
            try:
                fin_data, addr = connection.recvfrom(64)
                fin_data = PacketFactory.parseBytes(fin_data)
                if fin_data.fin == 1:
                    end_connection(connection,addr)
                    break
            except socket.timeout:
                connection.sendto(first_segment_ack.generatePacket(),addr)
                
    return 0
if __name__ == "__main__":
    run()