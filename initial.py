#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import tkinter as tk
from settings import settings
from tkinter.filedialog import askopenfilename

def send(listname, listloop, listshuffle):
    os.system('echo loadlist %s | %s' % (listname.get(), socat_cmd))
    if(listloop.get()):
        os.system('echo set loop-playlist yes | %s' % socat_cmd)
    if(listshuffle.get()):
        os.system('echo playlist-shuffle | %s' % socat_cmd)
    root.destroy()

def openfile(listname):
    options = {}
    options['filetypes'] = settings.filetypes
    options['initialdir'] = os.path.realpath(settings.default_dir)
    options['title'] = "Open a file list"
    options['parent'] = root

    root.withdraw()
    listname = askopenfilename(**options)
    return listname

def init():
    listloop = tk.BooleanVar(value=True)
    checkbox = tk.Checkbutton(root, text="playlist loop", variable=listloop, onvalue=True, offvalue=False).pack()
    listshuffle = tk.BooleanVar(value=True)
    checkbox2 = tk.Checkbutton(root, text="playlist shuffle", variable=listshuffle, onvalue=True, offvalue=False).pack()
    listname = tk.StringVar(value=settings.defaultlist)
    label = tk.Label(root, text=listname.get()).pack()
    fileselect = tk.Button(root, text="select", command=lambda l=listname : openfile(l)).pack()
    tk.Button(root, text="open", command=lambda l=listname, p=listloop, s=listshuffle : send(l, p, s)).pack()
    tk.mainloop()

def check():
    stat = os.system('systemctl --no-pager --user status mpv')
    if stat == 0:
        return True
    else:
        return False

def send_command():
    root.withdraw()

root=tk.Tk()
socat_cmd = "socat - %s" % settings.socketfile
if(not check()):
    os.system('systemctl --user start mpv')
    #send_command()
if (sys.argv[1] == 'open'):
    init()
elif (sys.argv[1] == 'restart'):
    os.system('systemctl --user restart mpv')
    init()
else:
    os.system("echo %s | %s" % (settings.commandlist[sys.argv[1]], socat_cmd))
