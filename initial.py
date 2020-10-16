#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from time import sleep
import tkinter as tk
import tkinter.messagebox
from settings import settings
from tkinter.filedialog import askopenfilename

class Control:
    def __init__(self, master=None):
        self.root = master
        self.listloop = tk.BooleanVar(value=settings.defaultloop)
        self.listshuffle = tk.BooleanVar(value=settings.defaultshuffle)
        self.listname = tk.StringVar(value=settings.defaultlist)
        self.listappend = tk.BooleanVar(value=settings.listappend)
        self.root.bind("<Escape>", lambda event : self.root.destroy())

    def load(self):
        self.checkbox = tk.Checkbutton(self.root, text="playlist loop", variable=self.listloop, onvalue=True, offvalue=False)
        self.checkbox.pack()
        self.checkbox2 = tk.Checkbutton(self.root, text="playlist shuffle", variable=self.listshuffle, onvalue=True, offvalue=False)
        self.checkbox2.pack()
        self.checkbox3 = tk.Checkbutton(self.root, text="playlist append", variable=self.listappend, onvalue=True, offvalue=False)
        self.checkbox3.pack()
        self.label = tk.Label(self.root, text=self.listname.get())
        self.label.pack()
        self.fileselect = tk.Button(self.root, text="select", command=self.openfile)
        self.fileselect.pack()
        self.openbox = tk.Button(self.root, text="open", command=self.send)
        self.openbox.pack()
        self.root.title("Load a playlist")
        self.root.bind("<Return>", lambda event : self.send())
        while(True):
            self.root.update()
            self.label['text'] = self.listname.get()

    def cmd(self):
        self.buttons = []
        self.root.title("Enter a command")
        row1 = tk.Frame(self.root)
        row1.pack(sid='top')
        row3 = tk.Frame(self.root)
        row3.pack(sid='bottom')
        row2 = tk.Frame(self.root)
        row2.pack(sid='bottom')
        for key in settings.buttonlist.keys():
            self.buttons.append(tk.Button(row1, text=settings.buttonlist[key], command= lambda _key=key : self.sendcmd(_key)))
        for button in self.buttons:
            button.pack(side='left')
        self.command = tk.StringVar()
        cmdput = tk.Entry(row2, text=self.command)
        cmdput.pack(side='left')
        cmdput.bind("<Return>", lambda event: self.sendcmd(cmdput.get()))
        cmdput.focus_set()
        cmdsend = tk.Button(row2, text='send', command= lambda : self.sendcmd(cmdput.get()))
        cmdsend.pack(side='left')
        cmdsend = tk.Button(row3, text='close', width=10, command=self.root.destroy)
        cmdsend.pack(side='left')

        self.root.mainloop()

    def send(self):
        if(self.listappend.get()):
            s_fileopen = os.system('echo loadlist %s append | %s' % (self.listname.get(), socat_cmd))
        else:
            s_fileopen = os.system('echo loadlist %s | %s' % (self.listname.get(), socat_cmd))
        if(self.listloop.get()):
            s_loop = os.system('echo set loop-playlist yes | %s' % socat_cmd)
        if(self.listshuffle.get()):
            s_shuffle = os.system('echo playlist-shuffle | %s' % socat_cmd)

        if s_fileopen + s_loop + s_shuffle != 0:
            tk.messagebox.showerror(title="Error", message="Command Send Failed!");

        self.root.destroy()

    def openfile(self):
        self.options = {}
        self.options['filetypes'] = settings.filetypes
        self.options['initialdir'] = os.path.realpath(settings.default_dir)
        self.options['title'] = "Open a file list"
        self.options['parent'] = self.root

        self.listname.set(askopenfilename(**self.options))

    def check(self):
        stat = os.system('systemctl --no-pager --user status mpv > /dev/null')
        if stat == 0:
            return True
        else:
            return False

    def sendcmd(self, cmd):
        sendcommand(cmd)
        if(cmd == "stop" or cmd == "quit"):
            self.root.destroy()
        self.command.set("")


def sendcommand(cmd):
    try:
        command = settings.commandlist[cmd]
        if(type(command) == list):
            for c in command:
                stat = os.system("echo %s | %s" % (c, socat_cmd))
        else:
            stat = os.system("echo %s | %s" % (command, socat_cmd))
    except KeyError:
        stat = os.system("echo %s | %s" % (cmd, socat_cmd))

    if stat != 0:
        tk.messagebox.showerror(title="Error", message="Command Send Failed!");

root=tk.Tk()
socat_cmd = "socat - %s" % settings.socketfile
app = Control(master=root)
if(not app.check()):
    os.system('systemctl --user start mpv')

if (sys.argv[1] == 'open'):
    app.load()

elif (sys.argv[1] == 'default'):
    #sleep(0.2)
    s_loop = os.system('echo set loop-playlist %s | %s' % ("yes" if settings.defaultloop else "no", socat_cmd))
    s_shuffle = os.system('echo %s | %s' % ("playlist-shuffle" if settings.defaultshuffle else "playlist-unshuffle", socat_cmd))
    s_fileopen = os.system('echo loadlist %s | %s' % (settings.defaultlist, socat_cmd))
    if s_fileopen + s_loop + s_shuffle != 0:
        tk.messagebox.showerror(title="Error", message="Command Send Failed!");

elif (sys.argv[1] == 'cmd'):
    app.cmd()

else:
    sendcommand(sys.argv[1])
