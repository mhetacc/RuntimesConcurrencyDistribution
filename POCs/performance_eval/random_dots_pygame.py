# Oss: "to blit" means to draw a source surface on top of a destination surface
# Surface.blit(what_to_draw, where_to_draw)
# where the second argument can either be (x,y) or Rect

from dataclasses import dataclass
import random
import pygame
import time

pygame.init()


GREY = (125, 125, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# create game window and set res 1000x1200
# COLxROW but its much easier to think in terms of x and y
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

############################ random points generation ############################
# can be enclosed in a function

# C-like struct that encapsulate both Rect and Surface of a point
@dataclass
class Point:
    prect: pygame.Rect
    psurface: pygame.Surface
    

# point is a square sized lxl
point_side_length = 30

# create a lot of Points and blit them
# to change number of point modify range() values
points = []
for i in range(1, 100):
    # create random point source (x0, y0)
    # offsets them to prevent going out of bounds
    point_x0 = random.randint(0, 1000 - point_side_length)
    point_y0 = random.randint(100, 1100 - point_side_length)

    # create point rect and surface
    point_rect = pygame.Rect(point_x0, point_y0, point_side_length, point_side_length)
    point_surface = pygame.Surface((point_side_length, point_side_length))

    # apply random color
    point_surface.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    # create Point
    point : Point = Point(point_rect, point_surface)
    
    # add to points list
    points.append(point)


# blit all points in the list
# for dev purposes: just to see that it works
for point in points:
    DISPLAY.blit(point.psurface, point.prect)

#################################################################################

# counters to measure fps
elapsed_frames = 0
last_frame_time = time.time()

fps_list = []
timestamp_list = []


# MAIN LOOP
while True:

    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


    ####################################### Do logical updates here.
    # ...

    # change each point coordinates 
    for point in points:
        # create random movement (+-5, +-5)
        movement = 5
        xmov = random.randint(-movement,movement)
        ymov = random.randint(-movement,movement)

        # must be that:
        #   0 + l/2 <= centerX <= 1000 - l/2
        # 100 + l/2 <= centerY <= 1100 - l/2

        if point.prect.centerx + xmov < point_side_length/2:
            xmov = movement
        if point.prect.centerx + xmov > 1000 - point_side_length/2:
            xmov = -movement
        
        if point.prect.centery + ymov < 100 + point_side_length/2:
            ymov = movement
        if point.prect.centery + ymov > 1100 - point_side_length/2:
            ymov = -movement
        
        # move in place Rect by the given offset
        point.prect.move_ip(xmov, ymov)


    ####################################### Render the graphics here.
    # ...

    # blit all points to their new positions
    # first draw over them the main display otherwise trace is left
    DISPLAY.blit(mainwindow, rect_main)
    for point in points:
        DISPLAY.blit(point.psurface, point.prect)



    pygame.display.flip()  # refresh on-screen display
    clock.tick(1000)       # sets framerate limit

    # print(clock.get_fps(), time.time())

    # print(fps + unix time)
    elapsed_frames += 1
    current_frame_time = time.time()
    if(current_frame_time - last_frame_time >= 1):
        print(f'fps = {elapsed_frames}', current_frame_time)

        fps_list.append(elapsed_frames)
        timestamp_list.append(current_frame_time)

        elapsed_frames=0
        last_frame_time = current_frame_time


with open('./logs/baseline_fps.txt', 'w') as file:
    


