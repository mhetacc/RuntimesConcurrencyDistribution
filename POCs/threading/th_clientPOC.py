from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
#import threading
import looping_timer

# have a timer which calls back print on the server side

class Client(SimpleXMLRPCServer):
    def __init__(self):
        super().__init__(('localhost',8080))
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000', allow_none=True)
                
        # timer must be last
        self.timer = looping_timer.LoopTimer(1.0, self.callback)
        self.timer.start()
        

    def callback(self):
        #self.proxy.server_print('client')
        print('callback')
        #self.timer.


########################################################

with Client() as client:

    client.serve_forever()