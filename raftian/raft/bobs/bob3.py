from xmlrpc.server import SimpleXMLRPCServer



with SimpleXMLRPCServer(('localhost', 8003), allow_none=True) as server:

 
    def server_print(string):
        print(string)

    server.register_function(server_print)

    server.serve_forever()



