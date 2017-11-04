#!/usr/bin/env python

#     http://0.0.0.0:8080/test?file=foo&signature=
#     12471c4ce67d411fff413a6b773cb3f0b091d765
# 
#     Copyright (C) 2015 Andrew J. Zimolzak <andyzimolzak@gmail.com>,
#     and licensed under GNU GPL version 3. Full notice is found in
#     the file 'LICENSE' in the same directory as this file.

import web
        
urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'World'
        params = web.input()
        if 'file' in params.keys() and 'signature' in params.keys():
            return('You are winner, ' + name
                   + '!\nYou get the file called: ' + params.file
                   + '\nBecause of your excellent ' + params.signature)
        else:
            return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
