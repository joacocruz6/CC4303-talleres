# Inspirado en :https://github.com/ValeryTyumen/DNS-Client
import struct
import random as r
import socket 
from dnslib import DNSRecord
import pprint
def to_bytes(value):
    return struct.pack('>H',value)
def to_normal(value):
    return struct.unpack('>H',value)
class MessageHeader(object):
    def __init__(self):
        self.message_id = r.randint(0,65535)
        self.qr = 0 # 0-> Query or 1-> response
        self.opcode = 0 # Codigo de la operacion, 0->Query, 1 -> IQUERY, 2 -> Status
        self.aa = 0 # 1 -> Authorative answer, 0 -> Non authorative
        self.tc = 0
        self.rd = 0
        self.ra = 0
        self.rcode = 0 # 0-> No error 1->Format Error 2-> Server Failure 3->Name error 4-> Not implemented 5->Refused
        self.qd_count = 1
        self.an_count = 0
        self.ns_count = 0
        self.ar_count = 0
    def __repr__(self):
        headers = f"""
ID:{self.message_id}
Query/Response:{self.qr}
OpCode:{self.opcode}
Authorative Answer:{self.aa}
TrunCation:{self.tc}
Recursion Desired:{self.rd}
Recursion Available:{self.ra}
Responce Code:{self.rcode}
Questions:{self.qd_count}
Answers:{self.an_count}
Authority RRs:{self.ns_count}
Additional RRs:{self.ar_count}
"""
        return headers
    def decode(self,message):
        self.messageID = to_normal(message[0:2]) # Primeros dos bits
        meta = to_normal(message[2:4])[0]
        self.rcode = meta & 15
        meta >>= 7
        self.ra = meta & 1
        meta >>= 1
        self.rd = meta & 1
        meta >>= 1
        self.tc = meta & 1
        meta >>= 1
        self.aa = meta & 1
        meta >>= 1
        self.opcode = (meta & 15)
        meta >>= 4
        self.qr = meta
        self.qd_count = to_normal(message[4:6])
        self.an_count = to_normal(message[6:8])
        self.ns_count = to_normal(message[8:10])
        self.ar_count = to_normal(message[10:12])
        return 12
    def encode(self):
        """ Genera la codificacion de los headers de una request DNS, a partir de lo que tiene guardado"""
        header = to_bytes(self.message_id)
        # Añado los headers en los bytes con un meta header
        meta = 0
        meta |= self.qr
        meta <<= 1
        meta |= self.opcode
        meta <<=4
        meta |= self.aa
        meta <<= 1
        meta |= self.tc
        meta <<= 1
        meta |= self.rd
        meta <<= 1
        meta |= self.ra
        meta <<= 7
        meta |= self.rcode
        header += to_bytes(meta)
        header += to_bytes(self.qd_count)
        header += to_bytes(self.an_count)
        header += to_bytes(self.ns_count)
        header += to_bytes(self.ar_count)
        return header
class MessageBody(object):
    def __init__(self,name: str):
        self.name = name
        self.type = 1 # 1 -> A
        self.request_class = 1 # 1 -> IN
    def __repr__(self):
        return f"Name: {self.name}\nType: {self.type}\nRequest Class: {self.request_class}"
    def encode(self):
        name = self.name
        if name.endswith('.'):
           name = name[:-1]
        name_bytes = b''
        for domain_name in name.split('.'):
            name_bytes += struct.pack('B',len(domain_name))
            name_bytes += bytes(domain_name,'utf-8')
        name_bytes += b'\x00'
        name_bytes += to_bytes(self.type)
        name_bytes += to_bytes(self.request_class)
        return name_bytes
class DNSMessage(object):
    def __init__(self,name):
        self.header = MessageHeader()
        self.question = MessageBody(name)
    def encode(self):
        message = b''
        message += self.header.encode()
        message +=self.question.encode()
        return message

# Funciones para decodear la respuesta
def decode_labels(message, offset):
    labels = []

    while True:
        length, = struct.unpack_from("!B", message, offset)

        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from("!H", message, offset)
            offset += 2

            return labels + decode_labels(message, pointer & 0x3FFF), offset

        if (length & 0xC0) != 0x00:
            raise StandardError("unknown label encoding")

        offset += 1

        if length == 0:
            return labels, offset

        labels.append(*struct.unpack_from("!%ds" % length, message, offset))
        offset += length


DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")

def decode_question_section(message, offset, qdcount):
    questions = []

    for _ in range(qdcount):
        qname, offset = decode_labels(message, offset)

        qtype, qclass = DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
        offset += DNS_QUERY_SECTION_FORMAT.size

        question = {"domain_name": qname,
                    "query_type": qtype,
                    "query_class": qclass}

        questions.append(question)

    return questions, offset
DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")
def decode_dns_message(message):

    id, misc, qdcount, ancount, nscount, arcount = DNS_QUERY_MESSAGE_HEADER.unpack_from(message)

    qr = (misc & 0x8000) != 0
    opcode = (misc & 0x7800) >> 11
    aa = (misc & 0x0400) != 0
    tc = (misc & 0x200) != 0
    rd = (misc & 0x100) != 0
    ra = (misc & 0x80) != 0
    z = (misc & 0x70) >> 4
    rcode = misc & 0xF

    offset = DNS_QUERY_MESSAGE_HEADER.size
    questions, offset = decode_question_section(message, offset, qdcount)

    result = {"id": id,
              "is_response": qr,
              "opcode": opcode,
              "is_authoritative": aa,
              "is_truncated": tc,
              "recursion_desired": rd,
              "recursion_available": ra,
              "reserved": z,
              "response_code": rcode,
              "question_count": qdcount,
              "answer_count": ancount,
              "authority_count": nscount,
              "additional_count": arcount,
              "questions": questions}

    return result

server = ["198.41.0.4"]
port = 3000
dns_port = 53
def run()->int:
    name = "www.google.com."
    message = DNSMessage(name)
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connection.settimeout(5)
    connection.connect((server[0],dns_port))
    query = message.encode()
    connection.send(query)
    response = connection.recv(1024)
    print(response)
    d = DNSRecord.parse(response)
    print(d)
    print("---------------------------------------------------------")
    print(d.header.a)
    print(d.auth)
    print(d.ar[0].rdata)
    connection.close()
    server[0] = str(d.ar[0].rdata)
    print(server[0])
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connection.connect((server[0],dns_port))
    connection.send(query)
    response = connection.recv(1024)
    print(response)
    d = DNSRecord.parse(responce)
    print(d)

    return 0
if __name__ == '__main__':
    run()