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

def addToFile(filename,addedtext):
    # Kalo mau nimpa semua, tinggal ganti a jadi r
    F = open(filename,"a")
    F.write(addedtext)
    F.close

def writeToFile(filename,addedtext):
    # Kalo mau nimpa semua, tinggal ganti a jadi r
    F = open(filename,"r")
    F.write(addedtext)
    F.close

def moveTempToActualLogs(src,dst):
    S = open(src,"r")
    # Fill commited logs file with temporary logs file
    while 1:
        line = S.readline()
        if not line:
            break
        log = line,"\n"
        addToFile(dst,log)
    S.close
    # Empty the temporary logs file
    writeToFile(src,"")

class LoadBalancer(BaseHTTPRequestHandler):
    # For Client Handling
    def do_POST(self):
        print "POST request"

    # For Each Node Communication
    def do_GET(self):
        global logcount
        global term
        try:
            args = self.path.split('/')
            if len(args) == 7:
                print "This is phase 3 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                logs = int(json_obj["commit"])
                if (commit == 1):
                    moveTempToActualLogs("tempLog.txt","commitedLog.txt")
                commitIndex = getLastLogIndex
                self.send_response(200)
                self.end_headers()
                signal.alarm(timeout_interval)
            elif len(args) == 6:
                print "This is phase 2 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                logs = json_obj["logs"]
                # INI UNTUK SAVE KE FILE EXTERNAL
                addToFile("logTemp.txt",logs)
                self.wfile.write(logs.encode('utf-8'))
                self.send_response(200)
                self.end_headers()
                signal.alarm(timeout_interval)
            elif len(args) == 5:
                print "This is phase 1 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                expectedTerm = int(json_obj["term"])
                expectedIndex = int(json_obj["index"])
                logarray = loadFile("commitedLog.txt")
                if (getTermFromIndex(logarray,expectedIndex) == expectedTerm):
                    self.wfile.write(expectedTerm,"/",expectedIndex,"/ok".encode('utf-8'))
                else:
                    self.wfile.write(expectedTerm,"/",expectedIndex,"no".encode('utf-8'))
                self.send_response(200)
                self.end_headers()
                signal.alarm(timeout_interval)
            elif len(args) == 4:
                print "This is phase 0 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                expectedNextIndex = int(json_obj["index"])
                log_array = loadFile("commitedLog.txt")
                realNextIndex = getLastLogIndex(log_array)+1
                self.wfile.write((expectedNextIndex,"/",realNextIndex).encode('utf-8'))
                self.send_response(200)
                self.end_headers()
                signal.alarm(timeout_interval)
            # Got election request
            elif len(args) == 3:
                global term
                print "This is election request for vote"
                currentIndex = 1 # TBD from logs
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                reqTerm = json_obj["term"]
                reqIndex = json_obj["index"]
                if (reqTerm > term):
                    if (reqIndex > currentIndex):
                        resp = reqTerm, "/1"
                        self.wfile.write(resp.encode('utf-8'))
                    else:
                        resp = reqTerm, "/-1"
                        self.wfile.write(resp.encode('utf-8'))
                    term += reqTerm
                else:
                    resp = reqTerm, "/-1"
                    self.wfile.write(resp.encode('utf-8'))
                self.send_response(200)
                self.end_headers()
                signal.alarm(timeout_interval)
            # Got request from client
            elif len(args) == 2:
                # Ask to daemon
                if (leader):
                    currentIndex += 1
                    indexLog = currentIndex," ____________________________________\n\n"
                    global workers
                    choosenWorkers = ""
                    minFreeMemory = 999999999999
                    for i in range(0,len(workers)):
                        sent = False
                        while (not sent):
                            print "Sending daemon request to ",workers[i]
                            conn = httplib.HTTPConnection(workers[i],":20000") # Address worker port 20000 is daemon
                            data = {}
                            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                            conn.request("GET", "/",json.dumps(data),headers)
                            r1 = conn.getresponse()
                            print r1.status, r1.reason
                            if (r1.status == "200"):
                                sent = True
                                data = response.read()
                                if (int(data) < min):
                                    min = int(data)
                                    choosenWorkers = workers[i]
                                dataLog[i] = "Address",i,": ",workers[i],"\nCPU Load1: ",data,"\n"
                            conn.close()
                    termLog = "term: ",term,"\n\n______________________________________"
                    fullLog = indexLog,dataLog,termLog
                    addToFile("logTemp.txt",fullLog)

                    # Send free address to Client
                    self.wfile.write(choosenWorkers.encode('utf-8'))
                    self.send_response(200)
                    self.end_headers()


        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

# Function called when time out occured
def timeOut(signum, frame):
    global allMatchIndex
    global allNextIndex
    global allPhase
    global leader
    global sumVote
    global term
    if (sumVote>0):
        leader = true
        sumVote = 0
        allMatchIndex = {0,0,0,0,0}
        nextIndex = getLastLogIndex(loadFile("commitedLog.txt")) + 1
        allNextIndex = {nextIndex,nextIndex,nextIndex,nextIndex,nextIndex}
        allPhase = {0,0,0,0,0}
    else:
        term += 1
        # Send leader election request
        signal.alarm(timeout_interval)
        for x in range(0,len(nodes)):
            if (x != nodenumber):
                currentIndex = 1 # TBD from logs
                print "Sending request to ",nodes[x]
                conn = httplib.HTTPConnection(nodes[x])
                data = {
                    "term": term,
                    "index": currentIndex
                }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/leader/election",json.dumps(data),headers)
                r1 = conn.getresponse()
                if (r1.status == 200):
                    data = response.read()
                    readData = data.split('/')
                    if (readData[0] == term):
                        sumVote += readData[1]
                else:
                    print r1.status, r1.reason


# FUNCTIONS FOR RETIEVE LOG
# BUT YOU NEED TO LOADFILE FIRST
# > log_array = loadFile(filename)

def getLog(log_array,index):
    return log_array[index]

def getTermFromIndex(log_array,index):
    return log_array[index][7]

def getLastLogIndex(log_array):
    return log_array[len(log_array)-1][0]

# Reminder
# log = log_array[index]
# Output dari fungsi ini tinggal dikirim aja, gausah diapa-apain lagi
def getJsonFromLog(log):
    data = {}
    # Index perlu ga?
    # data["index"] = log[0]
    data["address1"] = log[1]
    data["port1"] = log[2]
    data["cpu_load1"] = log[3]
    data["address2"] = log[4]
    data["port2"] = log[5]
    data["cpu_load2"] = log[6]
    data["term"] = log[7]
    json_data = json.dumps(data)
    return json_data

def leaderProcess(childNodeNumber): # TBD make as an thread for each child nodes
    print "Leader process", childNodeNumber, "\n"
    global allMatchIndex # TBD from logs
    global allNextIndex # TBD from logs then just fill the child node's with the same value as leader
    global allPhase
    while (1):
        if (leader):
            print "I am leader \n"
            # Getting index and term of child nodes
            # Already up to date
            if (steady):
                time.sleep(timeout_interval)
            if (allPhase[childNodeNumber] == 0):
                print "Sending next index to ",nodes[childNodeNumber]
                conn = httplib.HTTPConnection(nodes[childNodeNumber])
                data = {
                    "index": allNextIndex[childNodeNumber]
                }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/samain/next/index",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (r1.status != "200"):
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    steady = False
                    data = response.read()
                    readData = data.split('/') # Expected value -> next index/index result
                    # Check if no corrupted value
                    if (allNextIndex[childNodeNumber] == readData[0]):
                        if (allNextIndex[childNodeNumber] == readData[1]):
                            allPhase[childNodeNumber] = 1
                            allMatchIndex[childNodeNumber] = readData[1]-1 # Temporaly
                        else:
                            allNextIndex[childNodeNumber] -= 1
                conn.close()
            elif (allPhase == 1):
                term = allMatchIndex[childNodeNumber] # TBD from logs based on allMatchIndex
                print "Sending term and index to ",nodes[childNodeNumber]
                conn = httplib.HTTPConnection(nodes[childNodeNumber])
                data = {
                    "term": term,
                    "index": allMatchIndex[childNodeNumber]
                }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/samain/match/index/term",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (r1.status != "200"):
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    steady = False
                    data = response.read()
                    readData = data.split('/') # Expected value -> term/match index/ok||no
                    # Check if no corrupted value
                    if (term == readData[0]) and (allMatchIndex[childNodeNumber] == readData[1]):
                        if ("ok" == readData[2]):
                            allPhase[childNodeNumber] = 2
                        else:
                            allNextIndex[childNodeNumber] -= 1
                            allMatchIndex[childNodeNumber] -= 1
                conn.close()
            # Match index found -> Sending logs
            elif (allPhase[childNodeNumber] == 2):
                print "Sending necessary logs to ",nodes[childNodeNumber]
                log = "log"  # TBD retrieve logs from allMatchIndex[childNodeNumber]+1 up to current index one by one
                conn = httplib.HTTPConnection(nodes[childNodeNumber])
                data = {
                    "logs": log
                }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/ngasih/match/index/term/log",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (r1.status != "200"):
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    steady = False
                    data = response.read()
                    if (data == log):
                        allNextIndex[childNodeNumber] += 1
                        allMatchIndex[childNodeNumber] += 1
                    if (allMatchIndex[childNodeNumber] == currentIndex):
                        allPhase[childNodeNumber] = 3
                        steady = True
                conn.close()
            elif (allPhase[childNodeNumber] == 3):
                print "Just checking to ",nodes[childNodeNumber]
                log = "log"  # TBD retrieve logs from allMatchIndex[childNodeNumber]+1 up to current index one by one
                conn = httplib.HTTPConnection(nodes[childNodeNumber])
                sumCommit = 1
                for i in range(0,len(nodes)):
                    if (i != nodenumber) and (allPhase[i] == 3):
                        sumCommit += 1
                if (sumCommit >= 3):
                    commitIndex = allMatchIndex[childNodeNumber]
                    data = {
                        "commit": 1
                    }
                else:
                    data = {
                        "commit": 0
                    }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/index/term/log/check",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (r1.status != "200"):
                    allPhase[childNodeNumber] = 0
                if (allMatchIndex[childNodeNumber] != currentIndex):
                    allPhase[childNodeNumber] = 0
                    steady = False
                conn.close()

# INITIALIZERS
# How to RUN!!
# python load_balancer_zho.py NODENUMBER PORT TIMEOUTINTERVAL
if len(sys.argv) < 3:
    print "Should be >>\n\t python load_balancer_zho.py NODENUMBER TIMEOUTINTERVAL"
    sys.exit(1)

leader = False
nodenumber = int(sys.argv[1])
sumVote = 0
term = 0
allMatchIndex = {}
allNextIndex = {}
allPhase = {}
timeout_interval = int(sys.argv[2])

# Initialize daftar node
fileNode = open("node.txt","r")
nodes = []
while 1:
    line = fileNode.readline()
    if not line:
        break
    nodes.append(line)
fileNode.close

ipPort = nodes[nodenumber].split(":")
port = int(ipPort[1])
signal.signal(signal.SIGALRM, timeOut)
signal.alarm(timeout_interval)
server = HTTPServer(("", port), LoadBalancer)
print port
th = {}
for i in range(0,len(nodes)):
    if (i!=nodenumber):
        th[i] = threading.Thread(target=leaderProcess, kwargs={'childNodeNumber': i})
        th[i].daemon = True
        th[i].start()
server.serve_forever()
