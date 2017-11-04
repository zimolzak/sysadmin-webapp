#!/usr/bin/env python

#     http://0.0.0.0:8080/name?param1=val&param2=val
# 
#     Copyright (C) 2015 Andrew J. Zimolzak <andyzimolzak@gmail.com>,
#     and licensed under GNU GPL version 3. Full notice is found in
#     the file 'LICENSE' in the same directory as this file.

import web
import subprocess
        
urls = (
    '/(.*)', 'main_app'
)
app = web.application(urls, globals())

def cmds2string(cmdlist):
    output = ""
    separator = '\n\n~~~~\n\n'
    for c in cmdlist:
        output += subprocess.check_output(c) + separator
    return output

class main_app:        
    def GET(self, name):
        # `name` is what comes after the "/" and before "?"
        # params = web.input()
        # Gives you: pararms.keys(), param.keyname
        return cmds2string([["uptime"],
                            ["ps", "x"],
                            ["df", "-h"],
                            ["tail", "/home/pi/Desktop/local/Mulder-quote-generator/log.txt"],
                            ["cat", "/home/pi/Desktop/local/Mulder-quote-generator/pid.txt"]
                            ])

if __name__ == "__main__":
    app.run()
