import csv
from tkinter import *
from ctypes import windll, byref, create_unicode_buffer

import Usbhost # https://github.com/notiel/usbhost

# uses font Magic School One (c) 2004 Michael Hagemann

HOUSES = (("Gryffindor", '#900000'),
          ("Slytherin", '#008C45'),
          ("Ravenclaw", '#0000C9'),
          ("Hufflepuff", '#C09000'))
FILENAME = "points.csv"


def loadfont(fontpath):
    FR_PRIVATE  = 0x10
    pathbuf = create_unicode_buffer(fontpath)
    AddFontResourceEx = windll.gdi32.AddFontResourceExW

    flags = FR_PRIVATE
    AddFontResourceEx(byref(pathbuf), flags, 0)

def load_points():
    with open(FILENAME, "r", newline="") as file:
        reader = csv.reader(file)
        points = [int(p) for p in next(reader)]
        return points

def write_points(points):
    for i in range(len(points)):
        pts_lbls[i].config(text = points[i])

    command = "set %d %d %d %d\r\n" % tuple(points)
    ser = Usbhost.open_port(Usbhost.get_device_port())
    Usbhost.send_command(ser, command)
    Usbhost.close_port(ser)
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(points)

def setpoint(i):
    entry = e_set[i]
    txt = entry.get()
    entry.delete(0, 'end')
    try:
        n = int(txt)
    except ValueError:
        return
    points[i] = n
    write_points(points)
    
def pluspoint(i):
    entry = e_plus[i]
    txt = entry.get()
    entry.delete(0, 'end')
    try:
        n = int(txt)
    except ValueError:
        return
    points[i] += n
    write_points(points)
    
def minuspoint(i):
    entry = e_minus[i]
    txt = entry.get()
    entry.delete(0, 'end')
    try:
        n = int(txt)
    except ValueError:
        return
    points[i] -= n
    write_points(points)

def after_enter(event):
    entry = window.focus_get()
    if entry.t == "set":
        i = entry.num
        setpoint(i)
    elif entry.t == "plus":
        i = entry.num
        pluspoint(i)
    elif entry.t == "minus":
        i = entry.num
        minuspoint(i)
    

fontpath = "magic-school.one.ttf"
loadfont(fontpath)

points = load_points()

window = Tk()
window.title("Hogwarts points")
pts_lbls = []
e_set = []
e_plus = []
e_minus = []

window.bind('<Return>', after_enter)

lbl = Label(text="Задать новое количество баллов (нажмите Enter для ввода)")
lbl.grid(row=2, column=0, columnspan=8)

lbl = Label(text="Добавить баллы")
lbl.grid(row=4, column=0, columnspan=8)

lbl = Label(text="Отнять баллы")
lbl.grid(row=6, column=0, columnspan=8)


for c, house in enumerate(HOUSES):
    lbl = Label(text=house[0], font = ("magic school one", 30), foreground = house[1])
    lbl.grid(row=0, column=c*2, ipadx=10, ipady=6, padx=10, pady=10, columnspan=2)
    
    pts_lbl = Label(text=points[c], font=("Courier", 15))
    pts_lbl.grid(row=1, column=c*2, ipadx=10, ipady=6, padx=10, pady=10, columnspan=2)
    pts_lbls.append(pts_lbl)

    entry_set = Entry()
    entry_set.t = "set"
    entry_set.num = c
    e_set.append(entry_set)
    entry_set.grid(row=3, column=c*2, ipadx=20, ipady=6, pady=10, columnspan=2)

    lbl = Label(text="  +", font=("Courier", 15))
    lbl.grid(row=5, column=c*2, ipady=6, pady=10)
    entry_plus = Entry()
    entry_plus.t = "plus"
    entry_plus.num = c
    e_plus.append(entry_plus)
    entry_plus.grid(row=5, column=c*2 + 1, ipady=6, pady=10, padx=10)
    
    lbl = Label(text="  -", font=("Courier", 15))
    lbl.grid(row=7, column=c*2, ipady=6, pady=10)
    entry_minus = Entry()
    entry_minus.t = "minus"
    entry_minus.num = c
    e_minus.append(entry_minus)
    entry_minus.grid(row=7, column=c*2 + 1, ipady=6, pady=10, padx=10)
    
window.mainloop()
