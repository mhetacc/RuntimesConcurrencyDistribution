from pathlib import Path
from xmlrpc.server import SimpleXMLRPCServer
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


CREATE_SERVER = ('localhost', 8080)

# create server object with 'with' keyword so it closes as needed
# Oss: it actually create the server i.e. it does what python3 -m http does
with SimpleXMLRPCServer (CREATE_SERVER) as server:

    # create simple string return function 
    def test_foo(number):
        return f'The number is {number}'


    server.register_function(test_foo)

    server.serve_forever()