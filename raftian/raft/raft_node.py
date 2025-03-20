from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum
import reset_looping_timer
from dataclasses import dataclass
import random
import threading
import concurrent.futures
import xmlrpc.client



class Raft(SimpleXMLRPCServer):
    class Mode(Enum):
        LEADER = 1
        CANDIDATE = 2
        FOLLOWER = 3

    @dataclass
    class Entry:
        term: int
        index: int
        command: str 
    
    @dataclass
    class Server:
        id: int
        url: str
        port: int
        hp: int


    # class attributes here
    
    def __init__(self, addr, requestHandler = ..., logRequests = True, allow_none = False, encoding = None, bind_and_activate = True, use_builtin_types = False,
                 id : int = 0,
                 mode: Mode = 3,
                 timeout: float = 0.003,
                 cluster: list[Server] | None = None,
                 log: list[Entry] | None = None,
                 term: int | None = None,
                 cluster_config: int | None = None,
                 votes_count: int | None = None,
                 non_voter: bool = True,
                 voted_for: int | None = None,
                 commit_index: int | None = None,
                 last_applied: int | None = None,
                 next_index_to_send: list[int] | None = None,
                 last_index_on_server: list[int] | None = None
                 ):
        SimpleXMLRPCServer.__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate, use_builtin_types)

        # instance attributes here
        self.id: int = id
        self.mode: Raft.Mode = mode
        self.cluster: list[Raft.Server] | None = cluster
        self.log: list[Raft.Entry] | None = log
        self.term: int | None = term
        self.cluster_config: int | None = cluster_config
        self.votes_count: int | None = votes_count
        self.non_voter: bool = non_voter
        self.voted_for: int | None = voted_for
        self.commit_index: int | None = commit_index
        self.last_applied: int | None = last_applied
        self.next_index_to_send: list[int] | None = next_index_to_send
        self.last_index_on_server: list[int] | None = last_index_on_server

        # start timer
        self.timer = reset_looping_timer.LoopTimer(timeout, self.on_timeout)
        self.timer.start()
    

    def on_timeout(self):
        # TODO
        # switch self.mode 

        if self.mode == Raft.Mode.CANDIDATE:
            pass
        elif self.mode == Raft.Mode.LEADER:
            self.heartbeat()
        elif self.mode == Raft.Mode.FOLLOWER:
            pass
        else:
            print('Mode wrong') #TODO error message
        pass



    def append_entries_rpc(
            self,                   # self is serverproxy i.e., the client
            leader_term: int,
            leader_commit_index: int,
            #leader_id: int,        # to redirect other clients 
            leader_prev_log_index: int | None = None,
            leader_prev_log_term: int | None = None,
            entries: list[Entry] | None = None
    ) -> tuple[int, bool]:
        """
        Fired by leader, followers send back ack
        ack = (follower_term: int, entry_replicated: bool)

        Payload (i.e., entries) is either None (if used for propagating heartbeat) or a list of entries that have to be propagated on all followers

        TODO: must be moved outside of the class and registered by the client server
        with server.register_function(append_entries_rpc)
        """
        # HERE is what followers do

        # leader is still alive
        self.timer.reset()


        # if leader is out of date -> reject
        if leader_term < self.term:
            return (self.term, False)


        # if it was not just an heartbeat
        if entries is not None:

            # search in log an entry equal to prev_leader_entry
            # i.e., entry preceding future appended entries.
            # save its log index (!= entry index)
            entry_log_index: int | None = None
            for i, my_entry in enumerate(self.log):
                if (my_entry.index == leader_prev_log_index 
                    and my_entry.term == leader_prev_log_term):
                    entry_log_index = i
                    break # no need to search further


            # if follower does not have entry equal to prev_leader_entry -> reject
            if entry_log_index is None:
                return(self.term, False)


            # delete all log entries from the one equal to prev_leader_entry (excluded)
            del self.log[(entry_log_index + 1):]


            # append new entries
            self.log.append(entries)


            # update commit index
            if leader_commit_index > self.commit_index:
                self.commit_index = min(leader_commit_index,
                                        entries[-1].index
                                        )


        # everything went well
        return (self.term, True)
    
    

    def request_vote_rpc(
            self,
            candidate_term: int,
            candidate_id: int,
            candidate_last_log_index: int,
            candidate_last_log_term: int
    ) -> tuple[int, bool]:
        """
        Fired by candidates, other servers send back ack
        ack = (server_term: int, vote_granted: bool)

        Used to request vote from all servers in the cluster when a follower becomes a candidate and starts an election

        Depending on the result, candidate will either yield and revert to follower or become the new leader  
        """
        
        # HERE is what other servers do

        # if candidate less up to date -> reject
        if self.term > candidate_term:
            return (self.term, False)


        # if a candidate already exists
        if self.voted_for is not None and not candidate_id:
            return (self.term, False)
        

        # vote for candidate
        self.voted_for = candidate_id
        return (self.term, True)



    # on follower timeout
    def to_candidate(self):

        # become candidate, update term and vote for itself
        self.mode = Raft.Mode.CANDIDATE
        self.term += self.term
        self.voted_for = self.id
        

        # reset election timer
        # TODO check correctness of timer range
        timeout: float = random.uniform(0.0015, 0.002)
        self.timer.reset(timeout)


        # TODO
        # send request vote rpc to all servers in the cluster
        # how to make it non-blocking 
            

    def heartbeat(self):
        # send empty append_entries_rpc to all server proxies
        # TODO: is this correct or are we creating instances of servers everywhere?
        # TODO: use a threadpool

        # automatic blocking version

        results = []

        for i in range (0,len(self.cluster)):
            url: str = self.cluster[i].url
            port: int = self.cluster[i].port

            complete_url = 'http://' + str(url) + ':' + str(port)

            bob_proxy = xmlrpc.client.ServerProxy(complete_url, allow_none=True)

            results.append(bob_proxy.append_entries_rpc(self, self.term, self.commit_index))

        # threadpool executor version

        URLS: list[str] = []

        for i in range (0,len(self.cluster)):
            url: str = self.cluster[i].url
            port: int = self.cluster[i].port

            complete_url = 'http://' + str(url) + ':' + str(port)
            URLS.append(complete_url)

        
        # TODO ofcs remove
        URLS = ['http://www.foxnews.com/',
                'http://www.cnn.com/',
                'http://europe.wsj.com/',
                'http://www.bbc.co.uk/',
                'http://nonexistent-subdomain.python.org/']

        # Retrieve a single page and report the URL and contents
        def load_url(url, timeout):
            with urllib.request.urlopen(url, timeout=timeout) as conn:
                return conn.read()

        # from documentation:
        #  executor.submit(fn, /, *args, **kwargs) -> Future

        # Fire one append entries and return the result 
        def encapsulate_proxy(self, bob_url, term, commit_index) -> tuple[int, bool]:
            with xmlrpc.client.ServerProxy(bob_url, allow_none=True) as bob_proxy:
                 return bob_proxy.append_entries_rpc(self, term, commit_index)

        # We can use a with statement to ensure threads are cleaned up promptly
        # TODO always keep them around? maybe at __init__
        # SHOULD WORK
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster)) as executor:
            # Start the load operations and mark each future with its URL
            #future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
            future_to_url = {executor.submit(encapsulate_proxy, self, url, self.term, self.commit_index): url for url in URLS}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print('%r page is %d bytes' % (url, len(data)))



    # RUN method of the server
    def service_actions(self):

        # # apply log to state one at a time
        # # i.e., send to Pygame
        # if self.commit_index > self.last_applied:
        #     self.last_applied += self.last_applied
        #     #TODO 
        #     # try statement?
        #     # apply log[self.last_applied]


        return super().service_actions()
        

bob1 = Raft.Server(1, 'localhost', 8001, 100)
bob2 = Raft.Server(2, 'localhost', 8002, 100)
bob3 = Raft.Server(3, 'localhost', 8003, 100)
bob4 = Raft.Server(4, 'localhost', 8004, 100)

bobs_cluster : list[Raft.Server] = [bob1, bob2, bob3, bob4]

# enclose server in a callable function
def handle_server():
    with Raft(
        addr=('localhost', 8000),   # where server lives
        mode=1,                     # LEADER
        cluster=bobs_cluster,
        term=1000
        ) as server:
        def print_feedback(value):
            return value
        
        #server.register_function(print_feedback)
        server.serve_forever()






# pass all server stuff to a separate thread
thread = threading.Thread(target=handle_server)
thread.start()
