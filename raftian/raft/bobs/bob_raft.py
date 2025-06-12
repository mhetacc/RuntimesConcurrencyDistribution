from xmlrpc.server import SimpleXMLRPCServer
from enum import Enum
import reset_looping_timer
from dataclasses import dataclass
import random
import threading
import concurrent.futures
import xmlrpc.client
from queue import Queue
import pygame
import os
import signal
import time
import logging
from pathlib import Path
import datetime


############################## logs ###############################

# Oss: without bob1.py restart, writes in the same log file 

# logs are in the form "logs/filename/datetime.filename.log"
filename = 'bob_raft'

# create logger and makes it so that it record any message level
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')


logpath = Path(f'logs/{filename}/{datetime.datetime.now()}.{filename}.log')

# logger handler to sent all to correct path
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)

########################################################################

# testing purposes
# inside function explicit global keyword
pygame_commands = Queue()
pygame_commands.put('cmd1')
pygame_commands.put('cmd2')
pygame_commands.put('cmd3')
pygame_commands.put('cmd4')


# TODO: put class in separate file
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
                 mode: Mode = Mode.FOLLOWER,
                 timeout: float = 0.003,
                 cluster: list[Server] | None = None,
                 leader_id: int | None = None,
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
        self.leader_id: int | None = leader_id
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
        
        # internal attributes 
        self.last_propagated : time.time | None = None

        # start executors pool
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster))

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



    def propagate_entries(self):
        """
        Sends entries to all followers, for each of them traverse backwards through self.log until it finds the last common entry. 
        This is done passively: if follower reject entries, add last one not included from self.log and send again.

        TODO: this needs to be fired every .5s or so, hence either a separate looping timer or count timer clicks some way or another or fire from service actions() 
        """
        global pygame_commands


        if self.mode != Raft.Mode.LEADER:
            # all a follower is allowed to do is communicate its internal commands to the leader
            # leader will be responsible for propagation
            # meaning: followers do not apply commands immediately, but only when they are propagated back to them by the leader

            while not pygame_commands.empty():
                command = pygame_commands.get()
                self.new_entries.append(Raft.Entry(
                    term=self.term,
                    index=None,
                    command=command
                ))

            
            def encapsulate_proxy(self, leader: Raft.Server, entries) -> tuple[int, bool]:
                """Encapsulate all propagation procedure, fired with threadpool executor"""

                propagation_successful: bool = False    

                url: str = leader.url
                port: int = leader.port
                complete_url = 'http://' + str(url) + ':' + str(port)

                with xmlrpc.client.ServerProxy(complete_url, allow_none=True) as proxy:
                    while not propagation_successful:
                        # send new entries (local for each follower)    
                        result: tuple[bool, int] = proxy.append_entries_rpc(entries, self.term, self.commit_index)

                        # if leader is out of date  
                        if result[1] <= self.term:
                            self.to_candidate() #TODO
                        
                        if result[0] == True:
                            propagation_successful = True

                return propagation_successful


            results = []


            future_result = {self.executor.submit(encapsulate_proxy, self, server, entries, log_iterator): server for server in self.cluster if server.mode == Raft.Mode.LEADER}
            for future in concurrent.futures.as_completed(future_result):
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (future_result, exc))
                else:
                    print('Append result ', data)
                    results.append(data)


            if True in results:
                # there should be only one leader, so if True is in results, it means that entries were propagated successfully
                self.new_entries.clear()
            # else:
            #   new entries not cleaned, so they will be sent to Leader again
            
            

        ################################# LEADER mode #####################################
        else: 
            # translate pygame commands into entries to send 
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

            # here self.new_entries = [cmd1, cmd2, ... , cmdN]

            # travel backwards through self.log to search last entry not included in the follower log
            # use log_iterator for this purpose, soft resets for each follower
            entries: list[Raft.Entry] = self.new_entries
            log_iterator: int = -1

            def encapsulate_proxy(self, follower: Raft.Server, entries, log_iterator) -> tuple[int, bool]:
                """Encapsulate all propagation procedure, fired with threadpool executor"""

                propagation_successful: bool = False    

                url: str = follower.url
                port: int = follower.port
                complete_url = 'http://' + str(url) + ':' + str(port)

                with xmlrpc.client.ServerProxy(complete_url, allow_none=True) as proxy:
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
                            propagation_successful = True

                return propagation_successful


            results = []

            future_result = {self.executor.submit(encapsulate_proxy, self, follower, entries, log_iterator): follower for follower in self.cluster}
            for future in concurrent.futures.as_completed(future_result):
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (future_result, exc))
                else:
                    print('Append result ', data)
                    results.append(data)


            if results.count(True) >= len(self.cluster) / 2:
                self.log.extend(self.new_entries)
                self.new_entries.clear()
            # else:
            #   new entries not cleaned, so they will be propagated again
            
            

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

        def encapsulate_proxy(follower: Raft.Server, term, commit_index) -> tuple[int, bool]:
            """Encapsulate proxy fire it with a threadpool executor"""

            url: str = follower.url
            port: int = follower.port
            complete_url = 'http://' + str(url) + ':' + str(port)

            with xmlrpc.client.ServerProxy(complete_url, allow_none=True) as proxy:
                    return proxy.append_entries_rpc(None, term, commit_index)


        results = []


        # fire function using threadpool executor
        future_result = {self.executor.submit(encapsulate_proxy, follower, None, None): follower for follower in self.cluster}
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

        # propagate entries every 0.5 seconds
        if self.last_propagated is None:
            self.last_propagated = time.time()
        elif time.time() - self.last_propagated >= .5:
            # if pygame pipe not empty send commands to Leader
            global pygame_commands
            if not pygame_commands.empty():
                self.propagate_entries()
            self.last_propagated = time.time()

        
        
        

        return super().service_actions()
        


###################################################################################
################################       PYGAME      ################################
###################################################################################

def handle_pygame():
    global pygame_commands

    pygame.init()

    GREY = (125, 125, 125)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # create game window and set res 1000x1200
    DISPLAY = pygame.display.set_mode((1000, 1200))

    clock = pygame.time.Clock()

    # creates default font 
    font = pygame.font.Font(None, 60)

    # renders header and footer texts
    toptext = font.render("Top Text", False, BLACK)
    bottomtext = font.render("Bottom Text", False, BLACK)


    ############################### base surfaces #####################################

    # creates rects to constrain surfaces 
    # Rect((x0, y0), (width, height))
    rect_main = pygame.Rect(0, 100, 1000, 1000)
    rect_header = pygame.Rect(0, 0, 1000, 100)
    rect_footer = pygame.Rect(0, 1100, 1000, 100)

    # creates surfaces where UI elements are drawn upon
    # Surface((width, height))
    mainwindow = pygame.Surface((1000, 1000))
    header = pygame.Surface((1000, 100))
    footer = pygame.Surface((1000, 100))

    # color surfaces
    mainwindow.fill(GREY)
    header.fill(WHITE)
    footer.fill(WHITE)


    # vertical "game map" lines (on main window)
    pygame.draw.line(mainwindow, BLACK, (250, 0), (250, 1000), width=1)
    pygame.draw.line(mainwindow, BLACK, (500, 0), (500, 1000), width=1)
    pygame.draw.line(mainwindow, BLACK, (750, 0), (750, 1000), width=1)

    # horizontal "game map" lines (on main window)
    pygame.draw.line(mainwindow, BLACK, (0, 250), (1000, 250), width=1)
    pygame.draw.line(mainwindow, BLACK, (0, 500), (1000, 500), width=1)
    pygame.draw.line(mainwindow, BLACK, (0, 750), (1000, 750), width=1)


    # draw surfaces on DISPLAY surface "binded" on and by their respective rects
    # maybe rects were not necessary but they provide nice features nonetheless 
    DISPLAY.blit(mainwindow, rect_main) 
    DISPLAY.blit(header, rect_header)
    DISPLAY.blit(footer, rect_footer)

    ###################################################################################

    ########################### header and footer texts ###############################

    # since all boxes' positions starts from top left corner, to center them we
    # must calculate the offsets which are width/2 and height/2

    # header
    toptext_rect = toptext.get_rect()
    xoffset = toptext_rect.width/2
    yoffset = toptext_rect.height/2

    DISPLAY.blit(toptext, (rect_header.centerx - xoffset, rect_header.centery - yoffset))

    # footer
    bottomtext_rect = bottomtext.get_rect()
    xoffset = bottomtext_rect.width/2
    yoffset = bottomtext_rect.height/2

    DISPLAY.blit(bottomtext, (rect_footer.centerx - xoffset, rect_footer.centery - yoffset))

    #################################################################################

    #################################### players #################################### 
    player1 = pygame.Rect(585, 685, 80, 80)
    p1_ui = pygame.Surface((80,80))
    p1_ui.fill(RED)
    DISPLAY.blit(p1_ui, player1)

    player2 = pygame.Rect(835, 185, 80, 80)
    p2_ui = pygame.Surface((80,80))
    p2_ui.fill(GREEN)
    DISPLAY.blit(p2_ui, player2)

    player3 = pygame.Rect(335, 185, 80, 80)
    p3_ui = pygame.Surface((80,80))
    p3_ui.fill(BLUE)
    DISPLAY.blit(p3_ui, player3)

    player4 = pygame.Rect(85, 935, 80, 80)
    p4_ui = pygame.Surface((80,80))
    p4_ui.fill(YELLOW)
    DISPLAY.blit(p4_ui, player4)

    players = [player1, player2, player3, player4] # useful to extend to n players with randomized positions

    last_message_time = None

    # MAIN LOOP
    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.kill(os.getpid(), signal.SIGINT) # same as Ctrl+C, close also server thread 
                pygame.quit()
            
            if last_message_time is not None and time.time() - last_message_time >= .5:
                    # Reverts header to default text 
                    toptext = font.render(f"Top Text", False, BLACK)

                    # calculate offset
                    toptext_rect = toptext.get_rect()
                    xoffset = toptext_rect.width/2
                    yoffset = toptext_rect.height/2

                    # must first re-draw header surface otherwise previous text remains 
                    # then draws changed header text
                    DISPLAY.blit(header, rect_header)
                    DISPLAY.blit(toptext, (rect_header.centerx - xoffset, rect_header.centery - yoffset))
                    last_message_time = None

            # if mouse left button is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # gets mouse position
                pos = pygame.mouse.get_pos()

                for player in players:
                    if player.collidepoint(pos):
                        # starts timer to revert header text
                        last_message_time = time.time()

                        player_number = players.index(player) + 1

                        # change header text and renders it
                        toptext = font.render(f"Player {player_number} pressed", False, BLACK)
                        
                        # calculate offset
                        toptext_rect = toptext.get_rect()
                        xoffset = toptext_rect.width/2
                        yoffset = toptext_rect.height/2

                        # must first re-draw header surface otherwise previous text remains 
                        # then draws changed header text
                        DISPLAY.blit(header, rect_header)
                        DISPLAY.blit(toptext, (rect_header.centerx - xoffset, rect_header.centery - yoffset))



        # Do logical updates here.
        # ...


        # Render the graphics here.
        # ...


        # we want to limit display refresh speed
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # sets framerate

####################################################################################
####################################################################################


leader = Raft.Server(0, 'localhost', 8000, 100)
bob2 = Raft.Server(2, 'localhost', 8002, 100)
bob3 = Raft.Server(3, 'localhost', 8003, 100)
bob4 = Raft.Server(4, 'localhost', 8004, 100)

bobs_cluster : list[Raft.Server] = [leader] # testing purposes

# enclose server in a callable function
def handle_server():
    with Raft(
        addr=('localhost', 8005),   # where server lives
        mode=Raft.Mode.FOLLOWER,                     
        cluster=bobs_cluster,
        leader_id=1,
        timeout=0.5,                 # debugging purposes
        term=1,
        ) as server:


        def append_entries_rpc(entries: list[Raft.Entry], term: int, commit_index: int) -> tuple[bool, int]:

            ################################# FOLLOWER mode #####################################
            if server.mode != Raft.Mode.LEADER:
                # TODO
                logger.info(f"Received append_entries_rpc with term: {term} and commit_index: {commit_index}")
                logger.info(f"Entries: {entries}")  
                # Here you would implement the logic to handle the append entries RPC
                # For now, just return a success message
                #return (True, server.term)
            

            """
            Fired by leader, followers send back ack
            ack = (follower_term: int, entry_replicated: bool)

            Payload (i.e., entries) is either None (if used for propagating heartbeat) or a list of entries that have to be propagated on all followers

            TODO: must be moved outside of the class and registered by the client server
            with server.register_function(append_entries_rpc)
            """
            # HERE is what followers do

            # leader is still alive
            server.timer.reset()


            # if leader is out of date -> reject
            if term < server.term:
                return (False, server.term)


            # if it was not just an heartbeat
            if entries is not None:

                # search in log an entry equal to prev_leader_entry
                # i.e., entry preceding future appended entries.
                # save its log index (!= entry index)
                entry_log_index: int | None = None
                for i, my_entry in enumerate(server.log):
                    if (my_entry.index == entries[0].index 
                        and my_entry.term == entries[0].term):
                        entry_log_index = i
                        break # no need to search further


                # if follower does not have entry equal to prev_leader_entry -> reject
                if entry_log_index is None:
                    return(False, server.term)


                # delete all log entries from the one equal to prev_leader_entry (excluded)
                del server.log[(entry_log_index + 1):]


                # append new entries
                server.log.extend(entries)


                # update commit index
                if commit_index > server.commit_index:
                    server.commit_index = min (commit_index, entries[-1].index)


                # everything went well
                return (True, server.term)
 



            
            ################################# LEADER mode #####################################
            else:

                # if leader out of date
                    # reject
                    # revert to follower mode
                if term > server.term:
                    server.mode = Raft.Mode.FOLLOWER
                    return (False, server.term)
                
                # add commands to pygame_commands 
                # ack to follower
                for entry in entries:
                    pygame_commands.put(entry)

                logger.info(f"Leader received append_entries_rpc with term: {term} and commit_index: {commit_index}")
                logger.info(f"Received Entries: {entries}")  
                logger.info(f"Leader {server.id} pygame_commands = {pygame_commands}")
                
                return (True, server.term)
                
                


                
                
        server.register_function(append_entries_rpc)
        server.serve_forever()


# pass all server stuff to a separate thread
server_thread = threading.Thread(target=handle_server)
server_thread.start()

pygame_thread = threading.Thread(target=handle_pygame)
pygame_thread.start()

# safely terminate threads 
server_thread.join()
pygame_thread.join()