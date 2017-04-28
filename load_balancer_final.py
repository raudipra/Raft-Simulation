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
    # Kalo mau nimpa semua, tinggal ganti a jadi r
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

                # INI UNTUK SAVE KE FILE EXTERNAL
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

        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)


# Ini Buat baca file, baca paramnya sesuai urutan aja
# myarray = loadFile("test.txt")
# for log in myarray:
#     for x in log:
#         print x
#     print "______"

# Initialize daftar node
fileNode = open("node.txt","r")
nodes = {}
while 1:
    line = fileNode.readline()
    if not line:
        break
    nodes[i] = line
fileNode.close

# Function called when time out occured
def timeOut(signum, frame):
    global leader
    global sumVote
    global term
    if (sumVote>0):
        leader = true
        sumVote = 0
    else:
        term += 1
        # Send leader election request
        signal.alarm(timeout_interval)
        for x in range(0,len(nodes)):
            if (x != nodenumber):
                currentIndex = 1 # TBD from logs
                print "Sending request to ",nodes[x]
        		conn = httplib.HTTPConnection(node[x])
        		data = {
        		    "term": term
                    "index": currentIndex
        		}
        		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        		conn.request("GET", "/leaderElection",json.dumps(data),headers)
        		r1 = conn.getresponse()
        		print r1.status, r1.reason
                data = response.read()
                readData = data.split('/')
                if (readData[0] == term):
                    sumVote += readData[1]

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


def leaderProcess(): # TBD make as an thread for each child nodes
    print "Leader process"
    allMatchIndex = {0,0,0,0,0} # TBD from logs
    allNextIndex = {2,2,2,2,2} # TBD from logs then just fill the child node's with the same value as leader
    while (1):
        if (leader):
            for x in range(0,len(nodes)):
                if (x != nodenumber):
                    # Getting index and term of child nodes
                    # Already up to date
                    if (steady):
                        time.sleep(timeout_interval)
                    if (allPhase[x] == 0):
                        print "Sending next index to ",nodes[x]
                		conn = httplib.HTTPConnection(nodes[x])
                		data = {
                		    "index": allNextIndex[x]
                		}
                		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                		conn.request("GET", "/index/term",json.dumps(data),headers)
                		r1 = conn.getresponse()
                		print r1.status, r1.reason
                        if (r1.status != "200"):
                            allPhase[x] = 0
                            steady = True
                        else:
                            steady = False
                            data = response.read()
                            readData = data.split('/') # Expected value -> next index/index result
                            # Check if no corrupted value
                            if (allNextIndex[x] == readData[0]):
                                if (allNextIndex[x] == readData[1]):
                                    allPhase[x] = 1
                                    allMatchIndex[x] = readData[1]-1 # Temporaly
                                else:
                                    allNextIndex[x] -= 1
                        conn.close()
                    elif (allPhase == 1):
                        term = allMatchIndex[x] # TBD from logs based on allMatchIndex
                        print "Sending term and index to ",nodes[x]
                		conn = httplib.HTTPConnection(nodes[x])
                		data = {
                            "term": term
                		    "index": allMatchIndex[x]
                		}
                		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                		conn.request("GET", "/index/term",json.dumps(data),headers)
                		r1 = conn.getresponse()
                		print r1.status, r1.reason
                        if (r1.status != "200"):
                            allPhase[x] = 0
                            steady = True
                        else:
                            steady = False
                            data = response.read()
                            readData = data.split('/') # Expected value -> next index/index result
                            # Check if no corrupted value
                            if (term = readData[0]) && (allMatchIndex[x] == readData[1]):
                                if ("ok" == readData[2]):
                                    allPhase[x] = 2
                                else:
                                    allNextIndex[x] -= 1
                                    allMatchIndex[x] -= 1
                        conn.close()
                    # Match index found -> Sending logs
                    elif (allPhase[x] == 2):
                        print "Sending necessary logs to ",nodes[x]
                        log = "log"  # TBD retrieve logs from allMatchIndex[x]+1 up to current index one by one
                		conn = httplib.HTTPConnection(nodes[x])
                		data = {
                		    "logs": log
                		}
                		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                		conn.request("GET", "/index/term/log",json.dumps(data),headers)
                		r1 = conn.getresponse()
                		print r1.status, r1.reason
                        if (r1.status != "200"):
                            allPhase[x] = 0
                            steady = True
                        else:
                            steady = False
                            data = response.read()
                            if (data == log):
                                allNextIndex[x] += 1
                                allMatchIndex[x] += 1
                            if (allMatchIndex[x] == currentIndex):
                                allPhase[x] = 3
                                steady = True
                        conn.close()
                    elif (allPhase[x] == 3):
                        print "Just checking to ",nodes[x]
                        log = "log"  # TBD retrieve logs from allMatchIndex[x]+1 up to current index one by one
                		conn = httplib.HTTPConnection(nodes[x])
                        sumCommit = 1
                        for i in range(0,len(nodes)):
                            if (i != nodenumber) && (allPhase[i] == 3):
                                sumCommit += 1
                        if (sumCommit >= 3):
                            commitIndex = allMatchIndex[x]
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
                            allPhase[x] = 0
                        if (allMatchIndex[x] != currentIndex):
                            allPhase[x] = 0
                            steady = False
                        conn.close()
        time.sleep(timeout_interval)


signal.signal(signal.SIGALRM, timeOut)
signal.alarm(timeout_interval)
server = HTTPServer(("", PORT), WorkerHandler)
th = threading.Thread(target=leaderProcess)
th.daemon = True
th.start()
server.serve_forever()
