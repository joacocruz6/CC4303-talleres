# Inspirado en :https://github.com/ValeryTyumen/DNS-Client
import struct
import random as r
import socket 
from dnslib import DNSRecord
import sys
# TODO: Se puede hacer mas facil solo con dnslib
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


server_root = ["198.41.0.4"]
port = 3000 
dns_port = 53
def resolver(name: str):
    message = DNSMessage(name)
    server = server_root[0]
    while True:
        connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        connection.settimeout(5)
        connection.connect((server,dns_port))
        query = message.encode()
        connection.send(query)
        response = connection.recv(1024)
        d = DNSRecord.parse(response)
        if d.header.rcode == 0:
            if d.header.aa == 1:
                for x in d.rr:
                    if x.rtype == 1:
                        connection.close()
                        return d
                        #return str(x.rdata)
                break
            for x in d.ar:
                if x.rtype == 1:
                    server = str(x.rdata)
                    break
        else:
            connection.close()
            return d
        connection.close()
def run() -> int:
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_address = ('localhost',port)
    mysocket.bind(server_address)
    cache = list()
    cache_search = dict()
    while True:
        (data,address) = mysocket.recvfrom(1024)
        data = DNSRecord.parse(data)
        name = str(data.questions[0].get_qname())
        if name in cache_search:
            index = cache_search[name]
            ipdata = cache[index][1]
            cache.pop(index)
            cache.insert(index,(name,ipdata))
            ipdata.header.id = data.header.id
            mysocket.sendto(ipdata.pack(),address)
            print("Cacheado")
        else:
            ip = resolver(name)
            if len(cache) == 10:
                older_name = cache[9][0]
                del cache_search[older_name]
                cache.pop()
            
            for key in cache_search:
                cache_search[key] = cache_search[key] + 1
            cache_search[name] = 0
            cache.insert(0,(name,ip))    
            ip.header.id = data.header.id
            mysocket.sendto(ip.pack(),address)
        print(cache)
    #domain_name = sys.argv[1] +'.'
    #ipv4=resolver(domain_name)
    #print(ipv4)
    return 0
if __name__ == '__main__':
    run()