"""
Sends heartbeat to Bob while letting random_dots_pygame.py run.
Uses only threading module.
"""

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import looping_timer 
import threading
import datetime
import pygame

from dataclasses import dataclass
from pathlib import Path
import logging
import random
import time


class LoopingServer(SimpleXMLRPCServer):
    def __init__(self, uri, allow_none=True):
        self.heartbeat_timer = 0.003
        # creates itself (ie server start-up)
        SimpleXMLRPCServer.__init__(self, uri, allow_none)

        # gets a connection to another server via a client proxy
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8001', allow_none=True)
                
        self.timer = looping_timer.LoopTimer(self.heartbeat_timer, self.callback)
        self.timer.start()
        


    def callback(self):
        # sends periodic POST requests to node Bob 
        self.proxy.server_print('\n Alice\'s heartbeat: ' + str(datetime.datetime.now()) + '\n')

    




# enclose server in a callable function
def handle_server():
    with LoopingServer(('localhost', 8000)) as server:
        def print_feedback(value):
            return value
        
        server.register_function(print_feedback)
        server.serve_forever()





# pass all server stuff to a separate thread
thread = threading.Thread(target=handle_server)
thread.start()




###################################################################################
################################       PYGAME      ################################
###################################################################################

############################# logging ####################################

# logs are in the form "./logs/performance_evaluation/filename/datetime.filename_{number_of_dots}.log"
filename = 'threading_alice_peval'
number_of_dots = 1000 # used later, assigned now for path name

# create logger and makes it so that it record any message level
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, encoding='utf-8')


logpath = Path(f'logs/performance_evaluation/{filename}/{datetime.datetime.now()}.{filename}_{number_of_dots}.log')

# logger handler to sent all to correct path
filehandle = logging.FileHandler(logpath)
logger.addHandler(filehandle)

#########################################################################


pygame.init()


GREY = (125, 125, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# create game window and set res 1000x1200
# COLxROW but its much easier to think in terms of x and y
DISPLAY = pygame.display.set_mode((1000, 1200))

# necessary for fps limiting 
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

############################ random dots generation ############################
# can be enclosed in a function

# C-like struct that encapsulate both Rect and Surface of a dot
@dataclass
class Dot:
    drect: pygame.Rect
    dsurface: pygame.Surface
    

# dot is a square sized lxl
dot_side_length = 30

# create a lot of dots and blit them
# to change number of dot modify range() values
dots = []
for i in range(1, number_of_dots):
    # create random dot source (x0, y0)
    # offsets them to prevent going out of bounds
    dot_x0 = random.randint(0, 1000 - dot_side_length)
    dot_y0 = random.randint(100, 1100 - dot_side_length)

    # create dot rect and surface
    dot_rect = pygame.Rect(dot_x0, dot_y0, dot_side_length, dot_side_length)
    dot_surface = pygame.Surface((dot_side_length, dot_side_length))

    # apply random color
    dot_surface.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    # create dot
    dot : Dot = Dot(dot_rect, dot_surface)
    
    # add to dots list
    dots.append(dot)


# blit all dots in the list
# for dev purposes: just to see that it works
for dot in dots:
    DISPLAY.blit(dot.dsurface, dot.drect)

#################################################################################

# counters to measure fps
elapsed_frames = 0
last_frame_time = time.time()

# program timer: exits on timeout 
# 60*minutes = minutes of wait
timeout = time.time() + 60*5 + 2


# MAIN LOOP
while True:

    if time.time() > timeout:
        raise SystemExit

    # Process player inputs.
    # removed for log purposes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


    ####################################### Do logical updates here.
    # ...

    # change each dot coordinates 
    for dot in dots:
        # create random movement (+-5, +-5)
        movement = 5
        xmov = random.randint(-movement,movement)
        ymov = random.randint(-movement,movement)

        # must be that:
        #   0 + l/2 <= centerX <= 1000 - l/2
        # 100 + l/2 <= centerY <= 1100 - l/2

        if dot.drect.centerx + xmov < dot_side_length/2:
            xmov = movement
        if dot.drect.centerx + xmov > 1000 - dot_side_length/2:
            xmov = -movement
        
        if dot.drect.centery + ymov < 100 + dot_side_length/2:
            ymov = movement
        if dot.drect.centery + ymov > 1100 - dot_side_length/2:
            ymov = -movement
        
        # move in place Rect by the given offset
        dot.drect.move_ip(xmov, ymov)


    ####################################### Render the graphics here.
    # ...

    # blit all dots to their new positions
    # first draw over them the main display otherwise trace is left
    DISPLAY.blit(mainwindow, rect_main)
    for dot in dots:
        DISPLAY.blit(dot.dsurface, dot.drect)



    pygame.display.flip()  # refresh on-screen display
    clock.tick(1000)       # sets framerate limit


    # print(fps + unix time) and logs it
    elapsed_frames += 1
    current_frame_time = time.time()
    if(current_frame_time - last_frame_time >= 1):
        print(f'fps = {elapsed_frames}', current_frame_time)

        logger.info(f'time:{current_frame_time};fps:{elapsed_frames}')

        elapsed_frames=0
        last_frame_time = current_frame_time


   


