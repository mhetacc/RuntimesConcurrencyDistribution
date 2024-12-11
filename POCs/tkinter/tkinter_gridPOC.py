# grid may not be ideal since it is made to handle everything automatically 

# standard import behavior
from tkinter import *
from tkinter import ttk

# standard app window
root = Tk()
frame = ttk.Frame(root)

# connects geometry manager to frame
# use 4x4 grid, so with space for labels should be 6x4
# [    Label    ]
# [ ] [ ] [ ] [ ]
# [ ] [ ] [ ] [ ]
# [ ] [ ] [B] [ ]
# [ ] [ ] [ ] [ ]
# [    Label    ]
frame.grid()

# hook to display stuff
toptext = StringVar(master=frame, value='Top Text')

# label text default anchor=CENTER
# creates two labels that span all grid on x axis
ttk.Label(frame, textvariable=toptext).grid(column=0, row=0, columnspan=4)
ttk.Label(frame, text='Bottom Text').grid(column=0, row=5, columnspan=4)


button = Button(frame, background="red", width=1, height=1, command=lambda: toptext.set('Button Pressed'))


# loop to fix cell sizes of grid by implanting frame of exact dimensions
# not the best workaround but fine
for i in range(1,5):
    for j in range(0,4):
        # position of player
        if (i, j) == (3,2):
            button.grid(column=j, row=i)
        else:
            ttk.Frame(frame, width=200, height=200, 
            borderwidth=2, relief=RIDGE).grid(
                column=j,
                row=i
            )


# runs application
root.mainloop()