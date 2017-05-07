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

logarray = loadFile("commitedLog4.txt")
for log in logarray:
    print "\n\nLog"
    for x in log:
        print x
