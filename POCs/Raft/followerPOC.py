from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import time


class Follower(SimpleXMLRPCServer):
    def __init__(self, addr, name = None, cluster = [], log = [], heartbeat_received = False):
        super().__init__(addr)
        self.name = name
        self.cluster = cluster
        self.log = log
        self.heartbeat_received = heartbeat_received


    def append_entries(self, entry = ()):
        """Process received command"""
        self.heartbeat_received = True


        
        return True


    # @overrides
    # gets called in loop by serve_forever()
    def service_actions(self):
        """Loops indefinitely while waiting for a change to become leader"""
 
        time.sleep(1) 
        if (heartbeat_received == False):
            print('requestelection')

        heartbeat_received = False

        return super().service_actions()




# starts follower server
with Follower(('localhost', 8080)) as server:


    def append_entries(entry):
        """Exposes commands for client"""
        return server.append_entries(entry)

    server.register_function(append_entries)

    server.serve_forever()



