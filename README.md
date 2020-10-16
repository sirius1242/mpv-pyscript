## Simple script for mpv control
This is a script for opening mpv by systemd and sending command to control it.

### For First use
- move the mpv.service to ${HOME}/.config/systemd/user/
- type `systemctl --user daemon-reload`
- you can use `systemctl --user enable mpv` to make the service start at boot time, but no recommend.
- move the `settings.py.sample` to `settings.py` and edit settings.

### Usage
- use `python initial.py <command>` to execute certain command
- commands:
    - help: print the help message
    - open: open a play list
    - default: load default config
    - cmd: open sending command interface
- You can add key-value pair to commandlist in settings.py to add custom commands.