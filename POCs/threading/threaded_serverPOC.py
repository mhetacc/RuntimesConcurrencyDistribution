from xmlrpc.server import SimpleXMLRPCServer
import threading
import datetime
import time

# enclose server in a callable function
def handle_server():
    with SimpleXMLRPCServer(('localhost', 8080), allow_none=True) as server:
        def just_return(value):
            return value
        
        server.register_function(just_return)
        server.serve_forever()


# pass all server stuff to a separate thread
threading.Thread(target=handle_server).start()


# this is then allowed to run while server does so in a separate thread
while True:
    time.sleep(1)
    print(str(datetime.datetime.now()))