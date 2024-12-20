from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import looping_timer
import datetime


# by subclassing we can, if needed, override function run()
class LoopingServer(SimpleXMLRPCServer):
    def __init__(self):
        # creates itself (ie server start-up)
        SimpleXMLRPCServer.__init__(self, ('localhost',8080), allow_none=True)

        # gets a connection to another server via a client proxy
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000', allow_none=True)
                
        # timer must be last in the constructor
        self.timer = looping_timer.LoopTimer(1.0, self.callback)
        self.timer.start()
        

    def callback(self):
        # # while staying active as a server sends 
        # # periodic POST requests to another server
        # self.proxy.server_print('Sono le '+ str(datetime.datetime.now()))
        print('Sono le '+ str(datetime.datetime.now()))


########################################################

with LoopingServer() as loopserver:

    def just_return(message):
        return message
    
    loopserver.register_function(just_return)

    loopserver.serve_forever()