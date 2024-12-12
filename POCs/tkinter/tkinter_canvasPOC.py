# Oss: if window gets resized everything falls apart

from tkinter import *
from tkinter import ttk

# create root and place it in a grid
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create canvas, exact size, place it in the center of the grid
canvas = Canvas(root, width=1000, height=1000, background='gray75')
canvas.grid(column=0, row=1, sticky=(N, W, E, S))


# hook variable
toptext = StringVar(master=root, value='Top Text')


# header and footer placed in the grid
ttk.Label(root, textvariable=toptext).grid(column=0, row=0)
ttk.Label(root, text='Bottom Text').grid(column=0, row=2)


# visual grid creation
# horizontal lines
canvas.create_line(0,250, 1000,250, width=1)
canvas.create_line(0,500, 1000,500, width=1)
canvas.create_line(0,750, 1000,750, width=1)

# vertical lines
canvas.create_line(250,0, 250,1000, width=1)
canvas.create_line(500,0, 500,1000, width=1)
canvas.create_line(750,0, 750,1000, width=1)


# create button at (625, 625)
button = Button(canvas, background="red", width=1, height=1, command=lambda: toptext.set('Button Pressed'))

# must be put inside a canvas window
canvas.create_window(625,625, window=button)


root.mainloop()