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
filename = 'raft_node'

# create logger and makes it so that it record any message level
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')


logpath = Path(f'logs/{filename}/{datetime.datetime.now()}.{filename}.log')

# logger handler to sent all to correct path
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)

########################################################################

# user inputs trough Pygame which writes them here
# Raft reads them and propagate them to the cluster
pygame_commands = Queue()
#pygame_commands.put('cmd1')
#pygame_commands.put('cmd2')
#pygame_commands.put('cmd3')
#pygame_commands.put('cmd4')


# commands that have been applied to state are written here by Raft
# Pygame reads them and update UI accordingly 
raft_orders = Queue() 

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

    # class attributes here
    
    def __init__(self, 
                 addr: tuple[str, int],
                 allow_none: bool = True,
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
                 last_applied: int = -1,
                 next_index_to_send: list[tuple[int, int]] | None = None,
                 last_index_on_server: list[tuple[int, int]] | None = None
                 ):
        SimpleXMLRPCServer.__init__(self, addr=addr, allow_none=allow_none)

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
        self.last_applied: int = last_applied
        self.next_index_to_send: list[tuple[int, int]] | None = next_index_to_send
        self.last_index_on_server: list[tuple[int, int]] | None = last_index_on_server

        # internal attributes 
        self.countdown : time.time = time.time()  # used to countdown various actions, e.g. propagate entries every 0.5 seconds

        # start executors pool
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.cluster))

        # start timer
        self.timer = reset_looping_timer.LoopTimer(timeout, self.on_timeout)
        self.timer.start()

        
    

    def on_timeout(self):
        if self.mode == Raft.Mode.CANDIDATE:
            pass
        elif self.mode == Raft.Mode.LEADER:
            #self.heartbeat() 
            pass
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
            if self.log:
                entries: list[Raft.Entry] = []
                entries.append(self.log[-1])
                entries.extend(self.new_entries)
                log_iterator: int = -2
            else:
                entries: list[Raft.Entry] = self.new_entries
                log_iterator: int = -1


            def encapsulate_proxy(self: Raft, follower: Raft.Server, entries: list[Raft.Entry], log_iterator) -> tuple[bool, int]:
                """Encapsulate all propagation procedure, fired with threadpool executor"""

                propagation_successful: bool = False    

                url: str = follower.url
                port: int = follower.port
                complete_url = 'http://' + str(url) + ':' + str(port)

                with xmlrpc.client.ServerProxy(complete_url, allow_none=True) as proxy:
                    while not propagation_successful:
                        # send new entries (local for each follower)    

                        if proxy.is_log_empty():
                            # must propagate all log and all new entries
                            entries = self.log + entries

                        result: tuple[bool, int] = proxy.append_entries_rpc(entries, self.term, self.commit_index)
                        #logger.info(f'Append entries rpc result: {result}')

                        # if leader is out of date  
                        if result[1] > self.term:
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
                    results.append(data)


            if results.count(True) >= len(self.cluster) / 2:
                self.log.extend(self.new_entries)
                self.new_entries.clear()
                self.commit_index = self.log[-1].index  # IMPORTANT ensure that entries get applied

                #logger.info(f'Propagation successful')
                #logger.info(f'Leader: (commit index: {self.commit_index}, last_applied: {self.last_applied}), log = {self.log}')
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

        def encapsulate_proxy(follower: Raft.Server, leader_term, leader_commit_index) -> tuple[int, bool]:
            """Encapsulate proxy fire it with a threadpool executor"""

            url: str = follower.url
            port: int = follower.port
            complete_url = 'http://' + str(url) + ':' + str(port)

            with xmlrpc.client.ServerProxy(complete_url, allow_none=True) as proxy:
                    return proxy.append_entries_rpc(None, leader_term, leader_commit_index)


        results = []


        # fire function using threadpool executor
        future_result = {self.executor.submit(encapsulate_proxy, follower, self.term, self.commit_index): follower for follower in self.cluster}
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

        if time.time() - self.countdown >= .5:
            #logger.info('Service actions countdown expired')
            # do actions every 0.5 seconds
            global pygame_commands

            #logger.info(f'pygame_commands = {list(pygame_commands.queue)}')

            # propagate entries to cluster
            if not pygame_commands.empty():
                self.propagate_entries()

            #logger.info(f'self.new_entries = {self.new_entries}')

            # APPLY TO STATE 
            # i.e., traverse self.log between [last_applied, commit_index]
            # and add all entries to raft_orders Queue() 
            if self.commit_index is not None and self.commit_index > self.last_applied:   
                #logger.info('Applying entries to state')
                #logger.info(f'last_applied = {self.last_applied}, commit_index = {self.commit_index}, log = {self.log}')
                global raft_orders

                # first time anything gets applied to state
                if self.last_applied == -1:
                    raft_orders.put(self.log[0]) 
                    self.last_applied = self.log[0].index


                # find log index (!= entry.index) where last applied entry resides 
                last_applied_log_position: int = -1
                for i, my_entry in enumerate(self.log):
                    if (my_entry.index == self.last_applied):
                        last_applied_log_position = i
                        break # no need to search further
                
                #logger.info(f'last_applied_log_position = {last_applied_log_position}')
                #logger.info(f'log = {self.log}')
                

                # iterate trough remaining self.log until all entries between [last_applied, commit_index] are applied to state
                # i.e., they are written in raft_orders Queue()
                log_iterator = last_applied_log_position + 1

                while self.last_applied != self.commit_index:
                    #logger.info(f'log iterator = {log_iterator}')
                    raft_orders.put(self.log[log_iterator])
                    self.last_applied = self.log[log_iterator].index
                    log_iterator = log_iterator + 1
                # here self.last_applied == self.commit_index

                logger.info(f'Applied entries to state, raft_orders = {list(raft_orders.queue)}')
                #logger.info(f'last_applied = {self.last_applied}, commit_index = {self.commit_index}')

            # reset countdown
            self.countdown = time.time()


        return super().service_actions()
        
    


###################################################################################
################################       PYGAME      ################################
###################################################################################

def handle_pygame():



    pygame.init()

    pygame.display.set_caption(f'{filename}')  # set window title
    
    global pygame_commands  # write player inputs in this Queue
    global raft_orders      # read applied-to-state commands from this Queue

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
    @dataclass
    class Player:
        id: int
        hp: int
        rc: pygame.Rect     # represent player position and size and exposes useful methods like collidepoint()
        ui: pygame.Surface  # expose UI of the player e.g., colour 

    player1 = Player(
        id=1,
        hp=100,
        rc=pygame.Rect(585, 685, 80, 80),  # x, y, width, height
        ui=pygame.Surface((80,80))
    )
    player1.ui.fill(RED)
    DISPLAY.blit(player1.ui, player1.rc)

    player2 = Player(
        id=2,
        hp=100,
        rc=pygame.Rect(835, 185, 80, 80), # x, y, width, height
        ui=pygame.Surface((80,80))
    )
    player2.ui.fill(GREEN)
    DISPLAY.blit(player2.ui, player2.rc)

    player3 = Player(
        id=3,
        hp=100,
        rc=pygame.Rect(335, 185, 80, 80),  # x, y, width, height
        ui=pygame.Surface((80,80))
    )
    player3.ui.fill(BLUE)
    DISPLAY.blit(player3.ui, player3.rc)

    player4 = Player(
        id=4,
        hp=100,
        rc=pygame.Rect(85, 935, 80, 80),  # x, y, width, height
        ui=pygame.Surface((80,80))
    )
    player4.ui.fill(YELLOW)
    DISPLAY.blit(player4.ui, player4.rc)


    player_UI_cleaner = pygame.Surface((80, 80))  # used to clean player UI before re-blitting
    player_UI_cleaner.fill(WHITE)  

    players = [player1, player2, player3, player4] # useful to extend to n players with randomized positions


    last_message_time = None # used to revert header text after some time
    click_counter = 0

    # MAIN LOOP
    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # calls at the end of the loop
                os.kill(os.getpid(), signal.SIGINT) # same as Ctrl+C, close also server thread 


                

            # if mouse left button is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # gets mouse position
                pos = pygame.mouse.get_pos()

                for player in players:
                    if player.rc.collidepoint(pos):

                        if player.hp > 0:  
                            # starts timer to revert header text
                            last_message_time = time.time()

                            # change header text and renders it
                            toptext = font.render(f"Player {player.id} pressed", False, BLACK)

                            # add command to pygame_commands Queue
                            click_counter += 1
                            pygame_commands.put(player.id)  # put player id in the queue

                            # calculate offset
                            toptext_rect = toptext.get_rect()
                            xoffset = toptext_rect.width/2
                            yoffset = toptext_rect.height/2

                            # must first re-draw header surface otherwise previous text remains 
                            # then draws changed header text
                            DISPLAY.blit(header, rect_header)
                            DISPLAY.blit(toptext, (rect_header.centerx - xoffset, rect_header.centery - yoffset))
                        else:
                            # starts timer to revert header text
                            last_message_time = time.time()

                            # change header text and renders it
                            toptext = font.render(f"Player {player.id} already dead", False, BLACK)

                            # calculate offset
                            toptext_rect = toptext.get_rect()
                            xoffset = toptext_rect.width/2
                            yoffset = toptext_rect.height/2

                            # must first re-draw header surface otherwise previous text remains 
                            # then draws changed header text
                            DISPLAY.blit(header, rect_header)
                            DISPLAY.blit(toptext, (rect_header.centerx - xoffset, rect_header.centery - yoffset))



        # refresh header
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

        
        # apply state 
        while not raft_orders.empty():
            order: Raft.Entry = raft_orders.get()
            logger.info(f'order: {order}')

            for player in players:
                if player.id == order.command and player.hp > 0:
                    player.hp -= 30  # apply damage to player:

                    # modify player UI
                    if player.hp < 90 and player.hp >= 60:
                        player.ui.set_alpha(190)
                        DISPLAY.blit(player_UI_cleaner, player.rc)  # clean player UI
                        DISPLAY.blit(player.ui, player.rc)  # re-draw player UI
                    elif player.hp < 60 and player.hp >= 30:
                        player.ui.set_alpha(150)
                        DISPLAY.blit(player_UI_cleaner, player.rc)  # clean player UI
                        DISPLAY.blit(player.ui, player.rc)  # re-draw player UI
                    elif player.hp < 30 and player.hp > 0:
                        player.ui.set_alpha(100)
                        DISPLAY.blit(player_UI_cleaner, player.rc)  # clean player UI
                        DISPLAY.blit(player.ui, player.rc)  # re-draw player UI
                    elif player.hp <= 0:
                        player.ui.fill(BLACK)
                        player.ui.set_alpha(200)  
                        DISPLAY.blit(player.ui, player.rc)  # re-draw player UI
                
                logger.info(f'Player {player.id}, HP: {player.hp}')


        # we want to limit display refresh speed
        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # sets framerate



        # TODO for the future: 
        # if the game logic becomes more complex, it is better to separate the logic from UI updates
        # that being said, it requires more loops
####################################################################################
####################################################################################


bob1 = Raft.Server(1, 'localhost', 8001)
bob2 = Raft.Server(2, 'localhost', 8002)
bob3 = Raft.Server(3, 'localhost', 8003)
bob4 = Raft.Server(4, 'localhost', 8004)
bob_raft = Raft.Server(5, 'localhost', 8005)

bobs_cluster : list[Raft.Server] = [bob_raft] # testing purposes
#bobs_cluster : list[Raft.Server] = [bob1] # testing purposes


# enclose server in a callable function
def handle_server():
    with Raft(
        addr=('localhost', 8000),   # where server lives
        id=0,                        
        mode=Raft.Mode.LEADER,                     
        cluster=bobs_cluster,
        timeout=0.5,                 # debugging purposes
        term=1,
        ) as server:

        def append_entries_rpc(entries: list[Raft.Entry], term: int, commit_index: int) -> tuple[bool, int]:
            """
            Fired by servers, change behaviour depending on server.Mode
            returns ack = (replication_successful: bool, server_term: int)

            Mode.LEADER: Payload (i.e., entries) is either None (if used for propagating heartbeat) or a list of entries that have to be propagated on all followers;
            Mode.FOLLOWER: Payload is a list of entries that have to be appended to the follower's log. They will applied to state later when back-propagated by the leader. 

            Oss: Raft.Entry get transformed int dicts before being sent over the network, so they are not dataclasses anymore.
            """


            # unpack entries into a list of Raft.Entry objects
            tmp: list[Raft.Entry] = []
            for entry in entries:
                tmp.append(Raft.Entry(**entry))
            entries = tmp


            #logger.info('appended_entries_rpc received')
            ################################# FOLLOWER mode #####################################
            if server.mode != Raft.Mode.LEADER:
                #logger.info('Follower Mode')
                #logger.info(f'RPC : leader_term = {term}, leader_commit_index = {commit_index}, entries = {entries}')
                #logger.info(f'Follower: self.id = {server.id}, self.term = {server.term}, self.commit_index = {server.commit_index}, self.log = {server.log}')

                # leader is still alive
                server.timer.reset()


                # if leader is out of date -> reject
                if term < server.term:
                    return (False, server.term)

                # update commit index 
                if commit_index is not None and commit_index > server.commit_index:
                    server.commit_index = commit_index



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


                #logger.info('Everything went well')
                #logger.info(f'Follower: self.id = {server.id}, self.term = {server.term}, self.commit_index = {server.commit_index}, self.log = {server.log}')
                
                return (True, server.term)
    
            
            ################################# LEADER mode #####################################
            else:
                #logger.info('Leader Mode')
                #logger.info(f'terms: leader term = {server.term}, follower term = {term}')

                # if leader out of date reject and revert to follower mode
                if term > server.term:
                    server.mode = Raft.Mode.FOLLOWER
                    return (False, server.term)
                

                # add commands to pygame_commands 
                # ack to follower
                for entry in entries:
                    pygame_commands.put(entry)

                #logger.info(f"Leader received append_entries_rpc with term: {term} and commit_index: {commit_index}")
                #logger.info(f"Received Entries: {entries}")  
                #logger.info(f"Leader {server.id}, pygame_commands = {list(pygame_commands.queue)}")
                
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