#!/usr/bin/env python

import httplib
import sys
import time
import signal

#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

PORT = 13337
sumVote = 0
leader = 0
isVoted = 1

def handler(signum, frame):
    print "Forever is over!"
    if (sumVote>0):
        leader = 1
    

class WorkerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global isVoted
        try:
            args = self.path.split('/')
            if len(args) == 3:
                memoryClient1 = int(args[1])
                memoryClient2 = int(args[2])
                isVoted = 1
                signal.alarm(10)
                self.send_response(200)
                self.end_headers()  
            elif len(args) == 2:
                host = self.headers.get('Host')
                vote = int(args[1])
                if (vote == 3):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(str(isVoted).encode('utf-8'))
                    isVoted = 0
                    signal.alarm(10)
                elif (vote == 1):
                    self.send_response(200)
                    self.end_headers()
                    sumVote += 1
                    signal.alarm(10)
                elif (vote == 0):
                    self.send_response(200)
                    self.end_headers()
                    sumVote -= 1
                    signal.alarm(10)
            else:
                raise Exception()
            
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

signal.signal(signal.SIGALRM, handler)
signal.alarm(10)
server = HTTPServer(("", PORT), WorkerHandler)
server.serve_forever()

