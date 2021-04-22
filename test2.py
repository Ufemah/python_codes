import tkinter as tk
import datetime

root = tk.Tk()

can = tk.Canvas(height=500, width=1000)
can.pack()

rect = can.create_rectangle(0, 240, 20, 260, fil='#5F6A6A')


def act():
    global rect, can
    pos = can.coords(rect)
    if pos[2] < 1000:
        can.move(rect, 5, 0)
        can.update()
        can.after(1, act)
    else:
        can.after(1, act2)
        

def act2():
    global rect, can
    pos = can.coords(rect)
    if pos[3] < 500:
        can.move(rect, 0, 5)
        can.update()
        can.after(1, act2)
  

def key_down(key):
    act()
    

can.bind("<Button-1>", key_down)
root.mainloop()
