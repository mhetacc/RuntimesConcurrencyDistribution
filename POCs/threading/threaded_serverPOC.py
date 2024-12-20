from xmlrpc.server import SimpleXMLRPCServer
import threading
import datetime
import time



#with SimpleXMLRPCServer(('localhost', 8000), allow_none=True) as server:
#
# 
#    def server_print(string):
#        print(string)
#
#    server.register_function(server_print)
#
#    server.serve_forever()


def handle_server():
    with SimpleXMLRPCServer(('localhost', 8080), allow_none=True) as server:
        def just_return(value):
            return value
        
        server.register_function(just_return)
        server.serve_forever()



threading.Thread(target=handle_server).start()


while True:
    time.sleep(1)
    print(str(datetime.datetime.now()))