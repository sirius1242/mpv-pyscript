#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import tkinter as tk
from settings import settings
from tkinter.filedialog import askopenfilename

class Control:
    def __init__(self, master=None):
        self.root = master
        self.listloop = tk.BooleanVar(value=True)
        self.listshuffle = tk.BooleanVar(value=True)
        self.listname = tk.StringVar(value=settings.defaultlist)
        #root.mainloop()

    def load(self):
        self.checkbox = tk.Checkbutton(self.root, text="playlist loop", variable=self.listloop, onvalue=True, offvalue=False)
        self.checkbox.pack()
        self.checkbox2 = tk.Checkbutton(self.root, text="playlist shuffle", variable=self.listshuffle, onvalue=True, offvalue=False)
        self.checkbox2.pack()
        self.label = tk.Label(self.root, text=self.listname.get())
        self.label.pack()
        self.fileselect = tk.Button(self.root, text="select", command=self.openfile())
        self.fileselect.pack()
        self.openbox = tk.Button(self.root, text="open", command=self.send())
        self.openbox.pack()
        while(True):
            self.label['text'] = self.listname.get()
            self.root.update()
        #tk.mainloop()

    def send(self):
        if(self.listloop.get()):
            os.system('echo set loop-playlist yes | %s' % socat_cmd)
        if(self.listshuffle.get()):
            os.system('echo playlist-shuffle | %s' % socat_cmd)
        os.system('echo loadlist %s | %s' % (self.listname.get(), socat_cmd))
        self.root.destroy()

    def openfile(self):
        self.options = {}
        self.options['filetypes'] = settings.filetypes
        self.options['initialdir'] = os.path.realpath(settings.default_dir)
        self.options['title'] = "Open a file list"
        self.options['parent'] = self.root

        self.listname = askopenfilename(**self.options)

    def check(self):
        stat = os.system('systemctl --no-pager --user status mpv > /dev/null')
        if stat == 0:
            return True
        else:
            return False

root=tk.Tk()
socat_cmd = "socat - %s" % settings.socketfile
app = Control(master=root)
if(not app.check()):
    os.system('systemctl --user start mpv')
    #send_command()
if (sys.argv[1] == 'open'):
    app.load()

elif (sys.argv[1] == 'restart'):
    os.system('systemctl --user restart mpv')
    app.load()
else:
    os.system("echo %s | %s" % (settings.commandlist[sys.argv[1]], socat_cmd))
