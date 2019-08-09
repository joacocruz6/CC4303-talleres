require 'socket' # necesito la gema de sockets standard
require 'json'
require 'uri'

def run(json_file)
    proxy = TCPServer.open(8888)
    while true
        Thread.start(proxy.accept) do |client|
            file = File.read(json_file)
            json = JSON.parse(file)
            puts json['forbidden_words']
            request= client.readline
            STDERR.puts request
            verb    = request[/^\w+/]
            url     = request[/^\w+\s+(\S+)/, 1]
            version = request[/HTTP\/(1\.\d)\s*$/, 1]
            uri     = URI::parse url
            user = json['user']
            # Show what got requested
            puts((" %4s "%verb) + url)
            if json['blocked'].include? url
                client.print "HTTP/1.1 403\r\n"
                client.print "\r\n"
                client.print "Forbidden"
            else
                to_server = TCPSocket.new(uri.host, (uri.port.nil? ? 80 : uri.port))
                to_server.write("#{verb} #{uri.path}?#{uri.query} HTTP/#{version}\r\n")
                to_server.write("X-Elquepregunta: #{user}\r\n")
                content_length = 0
                loop do
                    line = client.readline # Tomo el resto de la peticion del cliente
                    if line =~ /^Content-Length:\s+(\d+)\s*$/
                        content_length = $1.to_i
                    end
                    if line =~ /^proxy/i
                        next
                      elsif line.strip.empty?
                        to_server.write("Connection: close\r\n\r\n")
                        
                        if content_length>= 0
                          to_server.write(client.read(content_length))
                        end
                        
                        break
                      else
                        to_server.write(line)
                      end
                end
                # Aca debo modificar para enviar el header por el que pregunta
                buff = ""
                loop do
                to_server.read(4048, buff)
                package = buff.split("\r\n\r\n")
                header = package[0]
                data = package[1]
                for x in json['forbidden_words']
                    for key in x.keys
                        data.gsub! key,x[key]
                    end
                end
                buff = header +"\r\n\r\n"+ data
                puts buff
                client.write(buff)
                break if buff.size < 4048
                end
                to_server.close()
            end
            client.close()
        end
    end
end
run(ARGV[0])