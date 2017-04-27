#!/usr/bin/env python

import httplib
import sys
import time
import signal
import psutil
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from array import *

allPrevTerm = {0,0,0,0,0}
allPrevIndex = {0,0,0,0,0}
allCommit = {0,0,0,0,0}
node = sys.args
index = 0
sumVote = 0
leader = 0
term = 0
isVoted = 1

def timeOut(signum, frame):
    global allPrevTerm
    print "Forever is over!"
    allPrevTerm[0] += 1
    for x in range(1,len(node)):
        params = urllib.urlencode({'term': allPrevTerm[0]})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection(node[x])
        conn.request("POST", "/", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        sumVote += data
    if (sumVote>0):
        leader = 1


class WorkerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print post_body
    def do_GET(self):
        global isVoted
        try:
            args = self.path.split('/')
            if len(args) == 4:
                termLeader = int(args[1])
                memoryClient1 = int(args[3])
                memoryClient2 = int(args[4])
                term = termLeader
                isVoted = 1
                signal.alarm(10)
                self.send_response(200)
                self.end_headers()
            elif len(args) == 2:
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

signal.signal(signal.SIGALRM, timeOut)
signal.alarm(10)
server = HTTPServer(("", node[0]), WorkerHandler)
server.serve_forever()

while (leader == 1):
    for x in range(1,len(node)):
        #Dapetin index sama term
        if (allCommit[x] == 0):
            params = urllib.urlencode({'index': allPrevIndex[0], 'term': allPrevTerm[0]})
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            conn = httplib.HTTPConnection(node[x])
            conn.request("POST", "/", params, headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            readData = data.split('/')
            if (allPrevIndex[x] == readData[0]) && (allPrevTerm == readData[1]):
                allCommit[x] = 1
            if (allPrevIndex[x] != readData[0])
                allPrevIndex[x] = readData[0]
            if (allPrevTerm[x] != readData[1])
                allPrevTerm[x] = readData[1]
            conn.close()
        elif (allCommit[x] == 1):
            #ambil semua log mulai dari allPrevIndex[x]
            params = urllib.urlencode({'index': allPrevIndex[x], 'term': allPrevTerm[x], 'log':log})
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            conn = httplib.HTTPConnection(node[x])
            conn.request("POST", "/", params, headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            if (data == "ok"):
                allCommit[x] = 2
            conn.close()
        time.sleep(10)
