#!/usr/bin/env python

# nohup ./webapp.py &

#     http://0.0.0.0:8080/name?param1=val&param2=val
# 
#     Copyright (C) 2015 Andrew J. Zimolzak <andyzimolzak@gmail.com>,
#     and licensed under GNU GPL version 3. Full notice is found in
#     the file 'LICENSE' in the same directory as this file.

import web
import subprocess
        
URLS = ('/(.*)', 'main_app')
APP = web.application(URLS, globals())
MULDER_LOG_FILE = "/home/pi/Desktop/local/Mulder-quote-generator/log.txt"
MULDER_PID_FILE = "/home/pi/Desktop/local/Mulder-quote-generator/pid.txt"

def cmds2string(cmdlist):
    output = ""
    separator = '\n\n~~~~\n\n'
    for c in cmdlist:
        if 'PSSPECIAL' in c:
            co = subprocess.check_output(["ps", "ax", "-o", "user,pid,tty,stat,time,command"])
            L = co.splitlines()
            L.sort()
            L_filt = []
            for e in L:
                if '[' in e:
                    continue
                else:
                    L_filt.append(e)
            output += '\n'.join(L_filt) + separator
        else:
            output += subprocess.check_output(c) + separator
    return output

# mulder bot.py
# webapp.py
# repeating_camera.py
# pid

class main_app:        
    def GET(self, name):
        # Not that this class uses it, but...
        # `name` is what comes after the "/" and before "?".
        # Whereas `params = web.input()`
        # gives you: pararms.keys(), param.keyname
        return cmds2string([["uptime"],
                            ["PSSPECIAL"],
                            ["df", "-h"],
                            ["tail", MULDER_LOG_FILE],
                            ["cat", MULDER_PID_FILE],
                            ])

if __name__ == "__main__":
    APP.run()
