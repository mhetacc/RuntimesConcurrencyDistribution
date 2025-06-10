from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum
import reset_looping_timer
from dataclasses import dataclass
import random
import threading
import concurrent.futures
import xmlrpc.client
from queue import Queue

# testing purposes
# inside function explicit global keyword
pygame_commands = Queue()
pygame_commands.put('cmd1')
pygame_commands.put('cmd2')
pygame_commands.put('cmd3')
pygame_commands.put('cmd4')



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
                 log: list[Entry] = [],
                 new_entries: list[Entry] = [],
                 term: int | None = None,
                 cluster_config: int | None = None,
                 votes_count: int | None = None,
                 non_voter: bool = True,
                 voted_for: int | None = None,
                 commit_index: int | None = None,
                 last_applied: int | None = None,
                 next_index_to_send: list[tuple[int, int]] | None = None,
                 last_index_on_server: list[tuple[int, int]] | None = None
                 ):
        SimpleXMLRPCServer.__init__(self, addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate, use_builtin_types)

        # instance attributes here
        self.id: int = id
        self.mode: Raft.Mode = mode
        self.cluster: list[Raft.Server] | None = cluster
        self.log: list[Raft.Entry] = log
        self.new_entries: list[Raft.Entry] = new_entries
        self.term: int | None = term
        self.cluster_config: int | None = cluster_config
        self.votes_count: int | None = votes_count
        self.non_voter: bool = non_voter
        self.voted_for: int | None = voted_for
        self.commit_index: int | None = commit_index
        self.last_applied: int | None = last_applied
        self.next_index_to_send: list[tuple[int, int]] | None = next_index_to_send
        self.last_index_on_server: list[tuple[int, int]] | None = last_index_on_server

        # # start executors pool
        # self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster))

        # start timer
        self.timer = reset_looping_timer.LoopTimer(timeout, self.on_timeout)
        self.timer.start()

        
    

    def on_timeout(self):
        # TODO
        # switch self.mode 

        if self.mode == Raft.Mode.CANDIDATE:
            pass
        elif self.mode == Raft.Mode.LEADER:
            #self.heartbeat()
            self.propagate_entries()    
        elif self.mode == Raft.Mode.FOLLOWER:
            pass
        else:
            print('Mode wrong') #TODO error message
        pass

    

    def TOBOB_append_entries_rpc(
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
 


    def propagate_entries(self):
        
        # print('##############################start##################################')
        # print(f'Leader log = {self.log}')
        # print(f'New entries = {self.new_entries}')

        # translate pygame commands into entries to send 
        global pygame_commands
        if not self.log:
            # if empty log the following next entry index will be 0
            log_index: int = -1 
        else:
            log_index: int = self.log[-1].index 

        while not pygame_commands.empty():
            command = pygame_commands.get()
            log_index += 1
            self.new_entries.append(Raft.Entry(
                term=self.term,
                index=log_index,
                command=command
            ))

        # print(f'Leader log = {self.log}')
        # print(f'New entries = {self.new_entries}')

        # here self.new_entries = [cmd1, cmd2, ... , cmdN]

        # travel backwards through self.log to search last entry not included in the follower log
        # use log_iterator for this purpose, soft resets for each follower
        entries: list[Raft.Entry] = self.new_entries
        log_iterator: int = -1
        # last_index: int = self.log[log_iterator].index        # un-necessary
        propagation_counter: int = 0


        # for each follower in the cluster
        for follower in self.cluster:

            url: str = follower.url
            port: int = follower.port
            complete_url = 'http://' + str(url) + ':' + str(port)

            proxy = xmlrpc.client.ServerProxy(complete_url, allow_none=True)
            
            propagation_successful: bool = False

            while not propagation_successful:
                # send new entries (local for each follower)    
                result: tuple[bool, int] = proxy.append_entries_rpc(entries, self.term, self.commit_index)

                # if leader is out of date
                if result[1] >= self.term:
                    self.mode = Raft.Mode.FOLLOWER
                    break
                
                if result[0] == False:
                    # add another entry from self.log to new entries
                    entries.append(self.log[log_iterator])
                    log_iterator -= 1   
                elif result[0] == True:
                    # increase propagation counter and move to next follower
                    propagation_counter += 1
                    propagation_successful = True
        
        if propagation_counter >= len(self.cluster) / 2:
            self.log.extend(self.new_entries)
            self.new_entries.clear()
        # else:
        #   new entries not cleaned, so they will be propagated again

        # print('############################end###################################')
        # print(f'Pygame commands = {pygame_commands}')
        # print(f'Leader log = {self.log}')
        # print(f'New entries = {self.new_entries}')
    
            




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
        """ 
        Gets fired by on_timeout() when in LEADER mode
        Calls empty append_entries_rpc() on all xmlrpc.client.ServerProxy 
        Takes urls and ports of proxies from self.cluster: list[Server]
        """

        # TODO: is this correct or are we creating instances of servers everywhere?


        # blocking version

        results = []

        if False:
            for i in range (0,len(self.cluster)):
                # one server proxy at a time 
                url: str = self.cluster[i].url
                port: int = self.cluster[i].port

                complete_url = 'http://' + str(url) + ':' + str(port)

                print('Complete URL= ',complete_url)

                bob_proxy = xmlrpc.client.ServerProxy(complete_url, allow_none=True)

                results.append(bob_proxy.append_entries_rpc(self.term, self.commit_index))

        #######################################################################
        # threadpool executor version

        URLS: list[str] = []

        for i in range (0,len(self.cluster)):
            # build URLs list 
            url: str = self.cluster[i].url
            port: int = self.cluster[i].port

            complete_url = 'http://' + str(url) + ':' + str(port)
            URLS.append(complete_url)


        def encapsulate_proxy(bob_url, term, commit_index) -> tuple[int, bool]:
            """Encapsulate proxy fire it with a threadpool executor"""
            with xmlrpc.client.ServerProxy(bob_url, allow_none=True) as bob_proxy:
                    return bob_proxy.append_entries_rpc(None, term, commit_index)


        results = []


        if False:
            pass
        # creates new concurrent futures wrapped in a with statement
        # i.e., with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster)) as executor:
        #     #     executor.submit
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster)) as executor:
            future_result = {executor.submit(encapsulate_proxy, url, None, None): url for url in URLS}
            for future in concurrent.futures.as_completed(future_result):
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (future_result, exc))
                else:
                    print('Append result ', data)
                    results.append(data)
        
        if False:
            # concurrent futures built-in version
            # i.e, self.executor.submit
            future_result = {self.executor.submit(encapsulate_proxy, url, None, None): url for url in URLS}
            for future in concurrent.futures.as_completed(future_result):
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (future_result, exc))
                else:
                    print('Append result ', data)
                    results.append(data)


        print('Results= ',results)


        # if leader is out of date, do nothing
        # followers will start election by themselves


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

bobs_cluster : list[Raft.Server] = [bob1] # testing purposes

# enclose server in a callable function
def handle_server():
    with Raft(
        addr=('localhost', 8000),   # where server lives
        mode=Raft.Mode.LEADER,                     
        cluster=bobs_cluster,
        #term=1000,
        timeout=0.5,                 # debugging purposes
        term=1,
        ) as server:
        def print_feedback(value):
            return value
        
        #server.register_function(print_feedback)
        server.serve_forever()


# pass all server stuff to a separate thread
thread = threading.Thread(target=handle_server)
thread.start()
thread.join()

