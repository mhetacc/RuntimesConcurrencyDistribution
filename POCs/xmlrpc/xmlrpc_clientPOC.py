from pathlib import Path
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



with xmlrpc.client.ServerProxy('http://localhost:8080', allow_none=True) as server:
    
    print(server.test_foo(42))  # working