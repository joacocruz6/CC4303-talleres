from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import sys
import json
class MyHttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        configFile = sys.argv[1]
        with open(configFile,'r') as f:
            configurations = json.load(f)
            self.send_response(200) # Envio el status de respuesta
            # Aca se envian los headers, 
            usuario = configurations['X-ElQuePregunta']
            self.send_header("X-ElQuePregunta",usuario)
            self.end_headers()
        return
    def do_HEAD(self):
        self.do_GET()


def run_server():
    host = 'localhost'
    port = 8888
    address = (host,port)
    httpd = ThreadingHTTPServer(address, MyHttpHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()