# xmlrpc.server with inside a xmlrpc.client 

from pathlib import Path
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import logging
import datetime


# logger related code 
# refer to POCs/loggingPOC.py for explanation
filename = 'xmlrpcPOC'
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logpath = Path(f'logs/{filename}/{datetime.datetime.now()}.{filename}.log')
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)


# different port from xmlrpc_serverPOC.py
CREATE_SERVER = ('localhost', 8000)

# create server object with 'with' keyword so it closes as needed
# Oss: it actually create the server i.e. it does what python3 -m http does
with SimpleXMLRPCServer (CREATE_SERVER) as server:

    # server without exposed functions

    with xmlrpc.client.ServerProxy('http://localhost:8080', allow_none=True) as proxy:
        print(proxy.test_foo(42))


    server.serve_forever()

