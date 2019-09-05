import socket


def run()-> int:
    port = 3000
    host = "127.0.0.1"
    my_app = (host,port)
    connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    connection.bind(my_app) 
    while True:
        data = connection.recv(64)
        print(data)
    return 0
if __name__ == "__main__":
    run()