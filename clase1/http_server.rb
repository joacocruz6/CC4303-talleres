require 'socket' # necesito la gema de sockets standard
require 'json'
def replace_forbidden(forbidden_words,text)
    return 
end
def run(json_file)
    server = TCPServer.open(8888)
    while true
        Thread.start(server.accept) do |client|
            file = File.read(json_file)
            json = JSON.parse(file)
            request = client.gets
            puts request
            info_request = request.split(" ")
            url = info_request[1]
            
            client.print "HTTP/1.1 200\r\n"
            client.print "user: #{json['user']}\r\n"
            client.print "Content-Type: text/html\r\n"
            client.print "\r\n"
            client.print "Hello World!"

            client.close()

        end
    end
end
run(ARGV[0])