#!/usr/bin/env python

import httplib
import sys
import time
import signal
import json

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
    
def loadFile(filename):
    F = open(filename,"r")
    n = 0
    array_log = []
    log = []
    while 1:
        line = F.readline()
        if not line:
            break
        #Line 1 : Index
        if (n % 7 == 0):
            log = []
            words = line.split(" ")
            log.append(words[0])
        #Line 2 & 6 & 7: ignore
        elif (n % 7 == 1 or n % 7 == 5 or n % 7 == 6):
            a = 1
        #Line 3: Address
        elif (n % 7 == 2):
            words = line.split(" ")
            log.append(words[1])
        #Line 4: Port
        elif (n % 7 == 3):
            words = line.split(" ")
            log.append(words[1])
        #Line 5: CPU Load
        elif (n % 7 == 4):
            words = line.split(" ")
            log.append(words[2])
            # Push to array_log
            array_log.append(log)
        n+=1    
    F.close
    return array_log

def writeToFile(filename,addedtext):
    F = open(filename,"a")
    F.write(addedtext)
    F.close

class WorkerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global logcount
        global isVoted
        try:
            args = self.path.split('/')
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            json_obj = json.loads(post_body)
            address = json_obj["address"]
            port = json_obj["port"]
            cpu_load = json_obj["cpu_load"]

            single_data_text = str(logcount)+" ____________________________________\n\n"
            single_data_text += "Address: "+address+" \n"
            single_data_text += "Port: "+ port+" \n"
            single_data_text += "CPU Load: "+ cpu_load+" \n"
            single_data_text += "\n______________________________________\n"
            print single_data_text
            writeToFile("test.txt",single_data_text)
            self.send_response(200)
            self.end_headers() 
            logcount+=1
            
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

# loadfile("test.txt")

logcount = 0
myarray = loadFile("test.txt")
for log in myarray:
    for x in log:
        print x


signal.signal(signal.SIGALRM, handler)
signal.alarm(10)
server = HTTPServer(("", PORT), WorkerHandler)
server.serve_forever()

