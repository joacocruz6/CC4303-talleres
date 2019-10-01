import struct
def createHeader(syn:int,ack: int,fin: int):
    header = 0
    header |= syn
    header <<= 1
    header |= ack
    header <<= 1
    header |= fin
    return header

def createData(data: str):
    return bytes("#"+data,"utf-8")


def decodeHeader(header):
    fin = header & 1
    header >>= 1
    ack = header & 1
    header >>= 1
    syn = header & 1
    return (syn,ack,fin)
def decodePacket(data_received):
    data_received = data_received.split(b"#")
    header = data_received[0]
    data = data_received[1]
    header = struct.unpack(">I",header)[0]
    header = decodeHeader(header)
    return (header[0],header[1],header[2],data)
def createPacket(syn: int, ack: int, fin: int,sequence_number:int,ack_number: int,data:bytes):
    packet = b''
    header = createHeader(syn,ack,fin)
    packet += struct.pack(">I",header)
    packet += createData(data)
    return packet