from xmlrpc.server import SimpleXMLRPCServer

# needs to be Raft node but with register_function(append_entries_rpc)

with SimpleXMLRPCServer(('localhost', 8002), allow_none=True) as server:

    def append_entries_rpc(entries, term, commit_index):
        print(f"Received append_entries_rpc with term: {term} and commit_index: {commit_index}")
        print(f"Entries: {entries}")
        # Here you would implement the logic to handle the append entries RPC
        # For now, just return a success message
        return (True, 0)

    server.register_function(append_entries_rpc)

    #results.append(bob_proxy.append_entries_rpc(self, self.term, self.commit_index))


    server.serve_forever()



