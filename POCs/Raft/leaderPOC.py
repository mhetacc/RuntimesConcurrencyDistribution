from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time


class Leader(SimpleXMLRPCServer):
    def __init__(self, addr, name = None, cluster = [], log = []):
        super().__init__(addr)
        self.name = name
        self.cluster = cluster
        self.log = log

    
    def propagate_entries(self, entry):
        """Sends entry to whole Raft cluster and counts acks
        entry = {
            key : attack / add / remove,
            player1: addr,
            player2: addr / None,
        }
        """
        
        acks = 0
        for follower in self.cluster:
            response = follower.append_entries(entry)
            acks += response # True to int


        if acks >= len(self.cluster) / 2:
            # commit
            # ie write in log
            pass

        return acks
    


    # @overrides
    # gets called in loop by serve_forever()
    def service_actions(self):
        """Loops indefinitely while sending heartbeats to Raft cluster"""

        # timer locks resource
        # process calls once unlock  
        time.sleep(5)
        print('heartbeat')
        #self.propagate_entries(None)

        return super().service_actions()


############################################################################

# starts leader server
with Leader(('localhost', 8000)) as server:


    # create simple string return function 
    def test_foo(number):
        return f'The number is {number}'

    server.register_function(test_foo)


    def send_command(cmd):
        """Exposes commands for client"""
        return server.propagate_entries(cmd)

    server.register_function(send_command)

    server.serve_forever()



