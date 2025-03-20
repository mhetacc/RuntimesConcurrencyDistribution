from xmlrpc.server import SimpleXMLRPCServer

# needs to be Raft node but with register_function(append_entries_rpc)

with SimpleXMLRPCServer(('localhost', 8001), allow_none=True) as server:

 
    def server_print(string):
        print(string)

    server.register_function(server_print)

    server.serve_forever()



