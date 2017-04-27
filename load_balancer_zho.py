#!/usr/bin/env python

import httplib
import sys
import time
import signal
import json
import threading

#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler


# sumVote = 0



# def handler(signum, frame):
#     print "Forever is over!"
#     if (sumVote>0):
#         leader = 1
    
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
    # For Client Handling
    def do_POST(self):
        print "POST request"

    # For Each Node Communication
    def do_GET(self):
        global logcount
        global isVoted
        global getrequest
        try:
            args = self.path.split('/')
            # Just To Make Sure, There's no way for access it directly
            # Should make it better way, fix it later rau.
            # Means it's sent by other nodes (maybe another better representation??)
            if len(args) == 5:
                getrequest = True
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
            # Means it's sent by daemon (maybe another better representation??)
            elif len(args) == 4:
                print "This is from daemon"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)

                machine_idx = json_obj["machine_idx"]
                cpu_load = json_obj["cpu_load"]

                print "Machine Idx: ",machine_idx
                print "CPU_LOAD: ",cpu_load,"\n"

                # Abis dapet data dari daemon diapain??
                # Nunggu semua machine ngabarin apa gmn?
                # Lanjutin rau, wieg
                # WKWKWKWKWK


                self.send_response(200)
                self.end_headers() 
            
        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)


# myarray = loadFile("test.txt")
# for log in myarray:
#     for x in log:
#         print x
#     print "______"


# INITIALIZERS
# How to RUN!!
# python load_balancer_zho.py NODENUMBER PORT TIMEOUTINTERVAL
if len(sys.argv) < 4:
    print "Should be >>\n\t python load_balancer_zho.py NODENUMBER PORT TIMEOUTINTERVAL"
    sys.exit(1)

leader = 0
isVoted = 1
logcount = 0
getrequest = False
nodenumber = int(sys.argv[1])
# PORT = 13337
PORT = int(sys.argv[2])
timeout_interval = int(sys.argv[3])

def NodeProcess():
    print "Node ",nodenumber," starting"
    global getrequest
    while (1):
        now = time.time()
        future = now + timeout_interval
        isTimeOut = True
        while time.time() < future:
            if (getrequest):
                isTimeOut = False
                getrequest = False
                break
                
        if (isTimeOut):
            print "Timeout"
        else:
            print "broken"
        

# signal.signal(signal.SIGALRM, handler)
# signal.alarm(10)
server = HTTPServer(("", PORT), WorkerHandler)
th = threading.Thread(target=NodeProcess)
th.daemon = True
th.start()
server.serve_forever()

