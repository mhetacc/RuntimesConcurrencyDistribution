import multiprocessing.pool
from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum
import reset_looping_timer
from dataclasses import dataclass
import random
import concurrent.futures




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
        pass



    def append_entries_rpc(
            self,                   # self is serverproxy i.e., the client
            leader_term: int,
            leader_commit_index: int,
            #leader_id: int,        # to redirect other clients 
            leader_prev_log_index: int,
            leader_prev_log_term: int,
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
            



    # RUN method of the server
    def service_actions(self):

        # apply log to state one at a time
        # i.e., send to Pygame
        if self.commit_index > self.last_applied:
            self.last_applied += self.last_applied
            #TODO 
            # try statement?
            # apply log[self.last_applied]


        return super().service_actions()
        


