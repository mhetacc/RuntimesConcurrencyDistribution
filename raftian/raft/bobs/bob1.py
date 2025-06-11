from xmlrpc.server import SimpleXMLRPCServer

from pathlib import Path
import logging
import datetime

############################## logs ###############################

# Oss: without bob1.py restart, writes in the same log file 

# logs are in the form "logs/filename/datetime.filename.log"
filename = 'bob1'

# create logger and makes it so that it record any message level
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')


logpath = Path(f'logs/{filename}/{datetime.datetime.now()}.{filename}.log')

# logger handler to sent all to correct path
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)

########################################################################


# needs to be Raft node but with register_function(append_entries_rpc)

with SimpleXMLRPCServer(('localhost', 8001), allow_none=True) as server:

    def append_entries_rpc(entries, term, commit_index):
        print(f"Received append_entries_rpc with term: {term} and commit_index: {commit_index}")
        print(f"Entries: {entries}")

        logger.info(f"Received append_entries_rpc with term: {term} and commit_index: {commit_index}")
        logger.info(f"Entries: {entries}")  
        # Here you would implement the logic to handle the append entries RPC
        # For now, just return a success message
        return (True, 0)

    server.register_function(append_entries_rpc)

    #results.append(bob_proxy.append_entries_rpc(self, self.term, self.commit_index))


    server.serve_forever()



