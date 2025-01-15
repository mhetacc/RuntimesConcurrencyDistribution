"""Node Alice do two things:
1. sends heartbeat to Bob every t-seconds
2. sends a different POST request when button inside game loop is pressed

Handles parallelism with multiprocessing instead of threading
"""

from xmlrpc.server import SimpleXMLRPCServer
import multiprocessing 
import xmlrpc.client
import looping_timer
import datetime
import pygame


# flag with appropriate thread safety
command_flag = multiprocessing.Event()
command_flag.clear()

class LoopingServer(SimpleXMLRPCServer):
    def __init__(self, uri, allow_none=True):
        self.heartbeat_timer = 3.0

        # creates itself (ie server start-up)
        SimpleXMLRPCServer.__init__(self, uri, allow_none)

        # gets a connection to another server via a client proxy
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8001', allow_none=True)
                
        self.timer = looping_timer.LoopTimer(self.heartbeat_timer, self.callback)
        self.timer.daemon = True # daemon thread gets destroyed on parent exit
        self.timer.start()
        


    def callback(self):
        # sends periodic POST requests to node Bob 
        self.proxy.server_print('\n Alice\'s heartbeat: ' + str(datetime.datetime.now()) + '\n')

    

    # called in loop by serve_forever()
    def service_actions(self):
        if command_flag.is_set():
            self.proxy.server_print('\n Alice\'s button pressed: ' + str(datetime.datetime.now()) + '\n')
            command_flag.clear()

        return super().service_actions()




# enclose server in a callable function
def handle_server():
    with LoopingServer(('localhost', 8000)) as server:
        def print_feedback(value):
            return value
        
        server.register_function(print_feedback)
        server.serve_forever()



# pass all server stuff to a separate process
process = multiprocessing.Process(target=handle_server)
process.start()



###################################################################################
################################       PYGAME      ################################
###################################################################################

pygame.init()

GREY = (125, 125, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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

# creates surfaces to be drawn upon ui elements
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
# must calculate the offsets which are of curse width/2 and height/2

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


# create "button" rect and its surface
# and blit it to display
rect_btn = pygame.Rect(585, 685, 80, 80)
button = pygame.Surface((80,80))
button.fill(RED)
DISPLAY.blit(button, rect_btn)



# MAIN LOOP
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        # if mouse left button is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # gets mouse position
            pos = pygame.mouse.get_pos()

            # test if a point (ie mouse) is inside the rectangle (ie button)
            if rect_btn.collidepoint(pos):
                
                # tells server that buttun has been pressed
                command_flag.set()

                # change header text and renders it
                toptext = font.render("Button Pressed", False, BLACK)

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


