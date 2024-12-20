from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading



with SimpleXMLRPCServer(('localhost', 8000), allow_none=True) as server:

 
    def server_print(string):
        print(string)

    server.register_function(server_print)

    server.serve_forever()



