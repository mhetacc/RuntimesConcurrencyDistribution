from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import datetime
import asyncio


class ATimer:
    """
    Scheduling periodic callbacks using handler
    Using call_later ensure that jobs dont get cancelled after timer stop()
    """
    def __init__(self, timeout, callback, args=None, kwargs=None):
        self._timeout = timeout
        self._callback = callback
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._loop = asyncio.get_event_loop()
        self._handler = None


    def _run(self):
        """Fire callback then restarts timer"""
        self._callback(*self._args, **self._kwargs)

        # call_later(timeout, callback)
        # calls callback after timeout runs out
        self._handler = self._loop.call_later(self._timeout, self._run)



    def start(self):
        self._handler = self._loop.call_later(self._timeout, self._run)

    def stop(self):
        self._handler.cancel()

    def reset(self):
        self.stop()
        self.start()



class LoopingServer(SimpleXMLRPCServer):
    def __init__(self, uri, allow_none=True):
        self.heartbeat_timer = 1

        # creates itself (ie server start-up)
        SimpleXMLRPCServer.__init__(self, uri, allow_none)

        # gets a connection to another server via a client proxy
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8001', allow_none=True)


        self.timer = ATimer(self.heartbeat_timer, self.callback)
        self.timer.start()
        


    def callback(self):
        # sends periodic POST requests to node Bob 
        self.proxy.server_print('\n Alice\'s heartbeat: ' + str(datetime.datetime.now()) + '\n')

    #async def service_actions(self):
    #    return super().service_actions()

    

async def handle_server():
    with LoopingServer(('localhost', 8000)) as server:
        server.serve_forever()


asyncio.run(handle_server())
