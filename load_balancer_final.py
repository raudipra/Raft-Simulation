#!/usr/bin/env python

import httplib
import sys
import time
import signal
import json
import threading
import random

#!/usr/bin/env python
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler

def loadFile(filename):
    # Function to read log file and load the content to array
    try:
        F = open(filename,"r")
        n = 0
        array_log = []
        log = []
        while 1:
            line = F.readline()
            if not line:
                break
            #Line 1 : Index
            if (n % 11 == 0):
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
    except IOError as e:
        return []

def addToFile(filename,addedtext):
    # Function to add string into log file txt
    # Replace 'a' into 'w' to overwrite the whole file
    F = open(filename,"a")
    F.write(addedtext)
    F.close

def writeToFile(filename,addedtext):
    # Function to write string into log file
    F = open(filename,"w")
    F.write(addedtext)
    F.close

def moveTempToActualLogs(src,dst):
    #Function to add temp into log file
    S = open(src,"r")
    # Fill commited logs file with temporary logs file
    while 1:
        line = S.readline()
        if not line:
            break
        log = line
        addToFile(dst,log)
    S.close
    # Empty the temporary logs file
    writeToFile(src,"")

class LoadBalancer(BaseHTTPRequestHandler):
    # For Client Handling
    def do_POST(self):
        print "POST request"
        log_array = loadFile("commitedLog"+str(nodenumber)+".txt")
        log = getLog(log_array, int(getLastLogIndex(log_array)))
        if (int(log[3]) >= int(log[6])):
            address_max = log[1]
            port_max = log[2]
        elif (int(log[3]) < int(log[6])):
            address_max = log[4]
            port_max = log[5]
        # Send address with max laod
        self.wfile.write(str(address_max)+":"+str(port_max))
        self.send_response(200)
        self.end_headers()


    # For Each Node Communication
    def do_GET(self):
        global term
        global machine_info
        try:
            args = self.path.split('/')
            #if len(args) == 7:

            #     print "This is phase 3 request"
            #     content_len = int(self.headers.getheader('content-length', 0))
            #     post_body = self.rfile.read(content_len)
            #     json_obj = json.loads(post_body)
            #     commit = int(json_obj["commit"])
            #     if (commit == 1):
            #         print "Commit!!!"
            #         moveTempToActualLogs("logTemp"+str(nodenumber)+".txt","commitedLog"+str(nodenumber)+".txt")
            #     # commitIndex = int(getLastLogIndex("commitedLog"+str(nodenumber)+".txt"))
            #     self.send_response(200)
            #     self.end_headers()
            #     signal.alarm(timeout_interval)

            if len(args) == 6: #length of param to identify kind of request
                # Entering the phase 2
                print "This is phase 2 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                print "INI RESPON JSON"
                print post_body
                json_obj = json.loads(post_body)
                # logs = json_obj["logs"]

                if json_obj: # If not empty
                    address1 = json_obj["address1"]
                    port1 = json_obj["port1"]
                    cpu_load1 = json_obj["cpu_load1"]
                    address2 = json_obj["address2"]
                    port2 = json_obj["port2"]
                    cpu_load2 = json_obj["cpu_load2"]
                    term = json_obj["term"]

                    # Format for the log file
                    currentIndex = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt")))
                    single_data_text = str(currentIndex+1)+" ____________________________________\n\n"
                    single_data_text += "Address1: "+address1+" \n"
                    single_data_text += "Port1: "+ port1
                    single_data_text += "CPU Load1: "+ cpu_load1+" \n"
                    single_data_text += "Address2: "+address2+" \n"
                    single_data_text += "Port2: "+ port2
                    single_data_text += "CPU Load2: "+ cpu_load2+" \n"
                    single_data_text += "Term: "+ term+" \n"
                    single_data_text += "\n______________________________________\n"
                    print single_data_text

                    # Save into log file
                    addToFile("commitedLog"+str(nodenumber)+".txt",single_data_text)

                # Send response
                self.wfile.write("/"+post_body+"/")
                self.send_response(200)
                self.end_headers()
                signal.alarm(random.randint(12, 20))
            elif len(args) == 5:
                # Entering the phase 1
                print "This is phase 1 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                expectedTerm = int(json_obj["term"])
                expectedIndex = int(json_obj["index"])
                logarray = loadFile("commitedLog"+str(nodenumber)+".txt")

                if (int(getTermFromIndex(logarray,expectedIndex)) == expectedTerm): # Match
                    self.wfile.write("/"+str(expectedTerm)+"/"+str(expectedIndex)+"/ok/")
                else:
                    self.wfile.write("/"+str(expectedTerm)+"/"+str(expectedIndex)+"/no/")

                self.send_response(200)
                self.end_headers()
                signal.alarm(random.randint(12, 20))
            elif len(args) == 4:
                # Entering the phase 0 initial phase
                print "This is phase 0 request"
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                expectedNextIndex = int(json_obj["index"])

                log_array = loadFile("commitedLog"+str(nodenumber)+".txt")
                realNextIndex = int(getLastLogIndex(log_array))+1
                self.wfile.write(("/"+str(expectedNextIndex)+"/"+str(realNextIndex)+"/"))

                self.send_response(200)
                self.end_headers()
                signal.alarm(random.randint(12, 20))
            # Got election request
            elif len(args) == 3:
                # Conduct voting
                print "This is election request for vote"
                currentIndex = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt")))
                content_len = int(self.headers.getheader('content-length', 0))
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                reqTerm = json_obj["term"]
                reqIndex = json_obj["index"]
                if (reqTerm > term):
                    if (reqIndex >= currentIndex):
                        resp = "/"+str(reqTerm)+"/1/"
                        self.wfile.write(resp)
                    else:
                        resp = "/"+str(reqTerm)+"/0/"
                        self.wfile.write(resp)
                    term += reqTerm
                else:
                    resp = "/"+str(reqTerm)+"/0/"
                    self.wfile.write(resp)
                self.send_response(200)
                self.end_headers()
                signal.alarm(random.randint(12, 20))
            # Got request from client

            elif len(args) == 2:
                # From daemon
                print "This is from daemon"
                if leader:
                    content_len = int(self.headers.getheader('content-length', 0))
                    post_body = self.rfile.read(content_len)
                    json_obj = json.loads(post_body)

                    machine_idx = json_obj["machine_idx"]
                    cpu_load = json_obj["cpu_load"]

                    print "Machine Idx: ",machine_idx
                    print "CPU_LOAD: ",cpu_load,"\n"

                    single_machine = []
                    if (len(machine_info) == 0):
                        # Hasnt received from daemon
                        single_machine.append(machine_idx)
                        single_machine.append(cpu_load)
                        machine_info.append(single_machine)
                        print "LEN MACHINE",str(len(machine_info))
                        logcount = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt"))) # TBD from log
                    elif (len(machine_info) == 1):
                        # Received from daemon
                        if machine_idx != machine_info[0][0]:
                            #
                            single_machine.append(machine_idx)
                            single_machine.append(cpu_load)
                            machine_info.append(single_machine)
                            print "LEN MACHINE",str(len(machine_info))
                            logcount = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt"))) # TBD from log
                            single_data_text = str(logcount+1)+" ____________________________________\n\n"
                            dummy = machines[int(machine_info[0][0])].split(":")
                            single_data_text += "Address1: "+dummy[0]+" \n"
                            single_data_text += "Port1: "+ dummy[1]
                            single_data_text += "CPU Load1: "+ str(machine_info[0][1])+" \n"
                            dummy = machines[int(machine_info[1][0])].split(":")
                            single_data_text += "Address2: "+dummy[0]+" \n"
                            single_data_text += "Port2: "+ dummy[1]
                            single_data_text += "CPU Load2: "+ str(machine_info[1][1])+" \n"
                            single_data_text += "Term: "+ str(term)+" \n"
                            single_data_text += "\n______________________________________\n"

                            addToFile("commitedLog"+str(nodenumber)+".txt",single_data_text)
                            machine_info[:] = []

                self.send_response(200)
                self.end_headers()


        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)


def timeOut(signum, frame):
    # Function called when time out occured
    global allMatchIndex
    global allNextIndex
    global allPhase
    global leader
    global sumVote
    global term
    global nodenumber
    global nodes
    print str(sumVote)+"ini sumvote \n"
    if (sumVote>=3):
        # Become leader when the vote is 3 or more
        print "Jadi leader"
        leader = True
        sumVote = 0
        allMatchIndex = [0,0,0,0,0]
        nextIndex = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt"))) + 1
        allNextIndex = [nextIndex,nextIndex,nextIndex,nextIndex,nextIndex]
        allPhase = [0,0,0,0,0]
    else:
        term += 1
        # Send leader election request
        signal.alarm(random.randint(5, 9))
        for x in range(0,len(nodes)):
            if (sumVote >= 3):
                signal.alarm(0)
                break
            if (x != nodenumber):
                currentIndex = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt"))) # TBD from logs
                print "Sending request to ",nodes[x]
                conn = httplib.HTTPConnection(nodes[x])
                data = {
                    "term": term,
                    "index": currentIndex
                }
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/leader/election",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (r1.status == 200):
                    data = r1.read()
                    readData = data.split('/')
                    print readData[1] + "Ini bagus \n"
                    if (int(readData[1]) == term):
                        print "masuk"
                        sumVote += int(readData[2])
                        print str(sumVote)+"ini sumvote \n"
                else:
                    print r1.status, r1.reason


# FUNCTIONS FOR RETIEVE LOG
# BUT YOU NEED TO LOADFILE FIRST
# > log_array = loadFile(filename)

def getLog(log_array,index):
    # Function to retrieve log from array based on index given as parameter
    if (not log_array):
        return ""
    else:
        return log_array[index]

def getTermFromIndex(log_array,index):
    # Function to retrieve term from array based on index given as parameter
    if (not log_array):
        return "0"
    else:
        return log_array[index][7]

def getLastLogIndex(log_array):
    # Function to retrieve last log
    if (not log_array):
        return "-1"
    else:
        return log_array[len(log_array)-1][0]

# Reminder
# log = log_array[index]
# Output dari fungsi ini tinggal dikirim aja, gausah diapa-apain lagi
def getJsonFromLog(log):
    # Function to retrieve Json from log
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
    steady = False
    while (1):
        currentIndex = int(getLastLogIndex(loadFile("commitedLog"+str(nodenumber)+".txt"))) # TBD from logs
        if (leader):
            print "I am leader \n"
            # Getting index and term of child nodes
            # Already up to date
            if (steady):
                time.sleep(random.randint(5, 9))
            if (allPhase[childNodeNumber] == 0):
                print "Sending next index to ",nodes[childNodeNumber]
                conn = httplib.HTTPConnection(nodes[childNodeNumber])
                data = {
                    "index": allNextIndex[childNodeNumber]
                }
                print "....alnextkecil ",allNextIndex[childNodeNumber]
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/samain/next/index",json.dumps(data),headers)
                r1 = conn.getresponse()
                print r1.status#, r1.reason
                if (int(r1.status) != 200):
                    print "Sini gan!!"
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    print "Bukan Sini gan!!"
                    steady = False
                    data = r1.read()
                    readData = data.split('/') # Expected value -> next index/index result
                    # Check if no corrupted value
                    print "ALL NEXT => ",allNextIndex[childNodeNumber]
                    i = 0
                    for m in readData:
                        print i," : ",m
                        i+=1
                    print "..."
                    if (allNextIndex[childNodeNumber] == int(readData[1])):
                        print "bukan bebas....."
                        if (allNextIndex[childNodeNumber] == int(readData[2])):
                            print "bebas....."
                            allMatchIndex[childNodeNumber] = int(readData[2])-1 # Temporaly
                            print "DEBUG BANG UDI",allMatchIndex[childNodeNumber],currentIndex
                            if (allMatchIndex[childNodeNumber] == currentIndex):
                                allPhase[childNodeNumber] = 0
                                steady = True
                                print "Masuk 0"
                            elif (allMatchIndex[childNodeNumber] == -1):
                                allPhase[childNodeNumber] = 2
                            else:
                                allPhase[childNodeNumber] = 1
                        else:
                            allNextIndex[childNodeNumber] -= 1
                conn.close()
            elif (allPhase[childNodeNumber] == 1):
                term = getTermFromIndex(loadFile("commitedLog"+str(nodenumber)+".txt"),allMatchIndex[childNodeNumber]) # TBD from logs based on allMatchIndex
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
                if (int(r1.status) != 200):
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    steady = False
                    data = r1.read()
                    readData = data.split('/') # Expected value -> term/match index/ok||no
                    # Check if no corrupted value
                    if (term == readData[1]) and (allMatchIndex[childNodeNumber] == int(readData[2])):
                        if ("ok" == readData[3]):
                            allPhase[childNodeNumber] = 2
                        else:
                            allNextIndex[childNodeNumber] -= 1
                            allMatchIndex[childNodeNumber] -= 1
                conn.close()
            # Match index found -> Sending logs
            elif (allPhase[childNodeNumber] == 2):
                print "Sending necessary logs to "+str(nodes[childNodeNumber])
                log_array = loadFile("commitedLog"+str(nodenumber)+".txt")
                log = getLog(log_array,allMatchIndex[childNodeNumber]+1) # TBD retrieve logs from allMatchIndex[childNodeNumber]+1 up to current index one by one
                conn = httplib.HTTPConnection(str(nodes[childNodeNumber]))
                data = getJsonFromLog(log)
                print "INI JSON NYA"
                print data
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                conn.request("GET", "/ngasih/match/index/term/log",data,headers)
                r1 = conn.getresponse()
                print r1.status, r1.reason
                if (int(r1.status) != 200):
                    allPhase[childNodeNumber] = 0
                    steady = True
                else:
                    steady = False
                    data = r1.read()
                    readData = data.split('/') # Expected value -> term/match index/ok||no
                    print "DEBUGGGGG!!!!"
                    print readData,"---------------"
                    print log,"---------------"
                    print "Masuk Nulis"
                    allNextIndex[childNodeNumber] += 1
                    allMatchIndex[childNodeNumber] += 1
                    if (allMatchIndex[childNodeNumber] == currentIndex):
                        allPhase[childNodeNumber] = 0
                        steady = True
                conn.close()
            else:
                print "Nah lho...",allPhase[childNodeNumber]

# INITIALIZERS
# How to RUN!!
# python load_balancer_zho.py NODENUMBER PORT TIMEOUTINTERVAL
if len(sys.argv) < 2:
    print "Should be >>\n\t python load_balancer_zho.py NODENUMBER"
    sys.exit(1)

leader = False
nodenumber = int(sys.argv[1])
sumVote = 1
logarray = loadFile("commitedLog"+str(nodenumber)+".txt")
currentIndex = int(getLastLogIndex(logarray))
term = int(getTermFromIndex(loadFile("commitedLog"+str(nodenumber)+".txt"),currentIndex))
commit = 0
allMatchIndex = []
allNextIndex = []
allPhase = []
machine_info = []

# Initialize daftar node
fileNode = open("node.txt","r")
nodes = []
while 1:
    line = fileNode.readline()
    if not line:
        break
    nodes.append(line)
fileNode.close

# Initialize daftar machine
fileMachine = open("machine.txt","r")
machines = []
while 1:
    line = fileMachine.readline()
    if not line:
        break
    machines.append(line)
fileMachine.close

ipPort = nodes[nodenumber].split(":")
port = int(ipPort[1])
signal.signal(signal.SIGALRM, timeOut)
signal.alarm(random.randint(12, 20))
server = HTTPServer(("", port), LoadBalancer)
print port
th = {}
for i in range(0,len(nodes)):
    if (i!=nodenumber):
        th[i] = threading.Thread(target=leaderProcess, kwargs={'childNodeNumber': i})
        th[i].daemon = True
        th[i].start()
server.serve_forever()
