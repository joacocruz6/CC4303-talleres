import socket
import sys
# Tamaño de los paquetes son de 64 bits
def run(message: str) -> int:
    host = "127.0.0.1"
    udp_port = 3000
    receiver = (host,udp_port)
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    connection.sendto(bytes(message,"utf-8"),receiver)
    return 0
if __name__ == "__main__":
    message = sys.argv[1]
    run(message)