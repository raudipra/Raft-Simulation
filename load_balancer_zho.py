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
        if (n % 12 == 0):
            log = []
            words = line.split(" ")
            log.append(words[0])
        #Line 2 & 10 & 11: ignore
        elif (n % 11 == 1 or n % 11 == 9 or n % 11 == 10):
            a = 1
        #Line 3: Address
        elif (n % 11 == 2):
            words = line.split(" ")
            log.append(words[1])
        #Line 4: Port
        elif (n % 11 == 3):
            words = line.split(" ")
            log.append(words[1])
        #Line 5: CPU Load
        elif (n % 11 == 4):
            words = line.split(" ")
            log.append(words[2])
            # Push to array_log
            array_log.append(log)
        #Line 6: Address
        elif (n % 11 == 5):
            words = line.split(" ")
            log.append(words[1])
        #Line 7: Port
        elif (n % 11 == 6):
            words = line.split(" ")
            log.append(words[1])
        #Line 8: CPU Load
        elif (n % 11 == 7):
            words = line.split(" ")
            log.append(words[2])
            # Push to array_log
            array_log.append(log)
        #Line 9: Term
        elif (n % 11 == 8):
            words = line.split(" ")
            log.append(words[1])
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
            address1 = json_obj["address1"]
            port1 = json_obj["port1"]
            cpu_load1 = json_obj["cpu_load1"]
            address2 = json_obj["address2"]
            port2 = json_obj["port2"]
            cpu_load2 = json_obj["cpu_load2"]
            term = json_obj["term"]

            single_data_text = str(logcount)+" ____________________________________\n\n"
            single_data_text += "Address1: "+address1+" \n"
            single_data_text += "Port1: "+ port1+" \n"
            single_data_text += "CPU Load1: "+ cpu_load1+" \n"
            single_data_text += "Address2: "+address2+" \n"
            single_data_text += "Port2: "+ port2+" \n"
            single_data_text += "CPU Load2: "+ cpu_load2+" \n"
            single_data_text += "Term: "+ term+" \n"
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
    print "______"


signal.signal(signal.SIGALRM, handler)
signal.alarm(10)
server = HTTPServer(("", PORT), WorkerHandler)
server.serve_forever()

