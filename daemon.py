import httplib, urllib
import json
import psutil,os
import sys
import time

# Port ganti jadi yang bener
registered_ports=[10001,10002,10007,10004,10005]

if len(sys.argv) < 2:
	print "Should be :"
	print "\t python daemon.py [machine_index]"
	sys.exit(1)

machine_idx = sys.argv[1]
p = psutil.virtual_memory()
freeMemory = p.free

while 1 :
	for port in registered_ports:
		address = "localhost:"+str(port)
		print "Sending machine detail to ",address
		conn = httplib.HTTPConnection(address)
		data = {
		    "machine_idx": machine_idx,
		    "cpu_load" : freeMemory
		}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn.request("GET", "/",json.dumps(data),headers)
		r1 = conn.getresponse()
		print r1.status, r1.reason
	time.sleep(6)
