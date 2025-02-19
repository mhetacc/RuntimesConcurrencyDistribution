from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum
import reset_looping_timer
from dataclasses import dataclass




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
                 mode: Mode = 3,
                 timeout: float = 0.003,
                 cluster: list[Server] = None,
                 log: list[Entry] = None,
                 term: int = None,
                 cluster_config: int = None,
                 votes_count: int = None,
                 non_voter: bool = True,
                 voted_for: int = None,
                 commit_index: int = None,
                 last_applied: int = None,
                 next_index_to_send: list[int] = None,
                 last_index_on_server: list[int] = None
                 ):
        SimpleXMLRPCServer.__init__(addr, requestHandler, logRequests, allow_none, encoding, bind_and_activate, use_builtin_types)

        # instance attributes here
        self.mode: Raft.Mode = mode
        self.cluster: list[Raft.Server] = cluster
        self.log: list[Raft.Entry] = log
        self.term: int = term
        self.cluster_config: int = cluster_config
        self.votes_count: int = votes_count
        self.non_voter: bool = non_voter
        self.voted_for: int = voted_for
        self.commit_index: int = commit_index
        self.last_applied: int = last_applied
        self.next_index_to_send: list[int] = next_index_to_send
        self.last_index_on_server: list[int] = last_index_on_server

        # start timer
        self.timer = reset_looping_timer.LoopTimer(timeout, self.on_timeout)
        self.timer.start()
    

    def on_timeout():
        # switch self.mode 
        pass

    def append_entries_rpc(
            leader_term: int,
            leader_commit_index: int,
            leader_id: int,
            prev_log_index: int,
            prev_log_term: int,
            entries: list[Entry] = None
    ) -> tuple[int, bool]:
        """
        Fired by leader, followers send back ack
        ack = (follower_term, entry_replicated)
        """
        # HERE is what followers do
        pass


