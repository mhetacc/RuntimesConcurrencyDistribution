# Oss: "to blit" means to draw a source surface on top of a destination surface
# blit(source, dest)

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


# Rect((x0, y0), (width, height))
# pos starts from top left vertex
# display = 1200x1000

point_l = 50

rect_btn = pygame.Rect(0, 100, point_l, point_l)
button = pygame.Surface((point_l,point_l))
button.fill(RED)
DISPLAY.blit(button, rect_btn)



################################ random point generation ####################################
# can be enclosed in a function

# point is a square lxl
point_side_length = 30

# create random point source
xval_point_source = random.randint(0,1000)
yval_point_source = random.randint(100,1100)

# offset source as needed
if xval_point_source + point_side_length > 1100:
    xval_point_source -= point_side_length
if yval_point_source + point_side_length > 1000:
    yval_point_source -= point_side_length

point_rect = pygame.Rect(xval_point_source, yval_point_source, point_side_length, point_side_length)
point = pygame.Surface((point_side_length, point_side_length))
point.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
DISPLAY.blit(point, point_rect)


# counters to measure fps
elapsed_frames = 0
last_frame_time = time.time()

# MAIN LOOP
while True:

    mouse_pos=None

    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        # if mouse left button is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # gets mouse position
            mouse_pos = pygame.mouse.get_pos()

            # test if a point (ie mouse) is inside the rectangle (ie button)



    # Do logical updates here.
    # ...


    # Render the graphics here.
    # ...

    if mouse_pos is not None and rect_btn.collidepoint(mouse_pos):
                
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





    # we want to limit display refresh speed
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(10)         # sets framerate

    #print(clock.get_fps(), time.time())

    elapsed_frames += 1
    current_frame_time = time.time()
    if(current_frame_time - last_frame_time >= 1):
        print(f'fps = {elapsed_frames}', current_frame_time)
        elapsed_frames=0
        last_frame_time = current_frame_time




