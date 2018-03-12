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

def special_list():
    co = subprocess.check_output(["ps", "ax", "-o", "user,pid,tty,stat,time,command"])
    L = co.splitlines()
    L.sort()
    L_filt = []
    for e in L:
        if '[' in e:
            continue
        else:
            L_filt.append(e)
    return '\n'.join(L_filt)

PS_AX = special_list()

def cmds2string(cmdlist):
    output = ""
    separator = '\n\n~~~~\n\n'
    for c in cmdlist:
        if 'BASICSPECIAL' in c:
            output += basic_statuses(PS_AX) + separator
        elif 'PSSPECIAL' in c:
            output += PS_AX + separator
        else:
            output += subprocess.check_output(c) + separator
    return output

def pid_contents():
    return subprocess.check_output(["cat", MULDER_PID_FILE])

def basic_statuses(ps_string):
    result = ''
    py_searches = ['bot.py', 'webapp.py', 'repeating_camera.py']
    python_lines = []
    for L in ps_string.splitlines():
        if 'python' in L:
            python_lines.append(L)
    for psearch in py_searches:
        for pl in python_lines:
            true_false = str(psearch in pl)
            result += (psearch + ': ' + true_false + '\n')
    true_false = str(pid_contents() in ps_string)
    result += ('PID matches: ' + true_false + '\n')
    return result

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
        
        return cmds2string([["BASICSPECIAL"],
                            ["uptime"],
                            ["PSSPECIAL"],
                            ["df", "-h"],
                            ["tail", MULDER_LOG_FILE],
                            ["cat", MULDER_PID_FILE],
                            ])

if __name__ == "__main__":
    APP.run()
