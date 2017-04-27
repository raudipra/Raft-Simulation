import httplib, urllib
import json
import psutil,os
import sys
import time

# Port ganti jadi yang bener
registered_ports=[13337,8080,7341,13237,13376]

if len(sys.argv) < 2:
	print "Should be :"
	print "\t python daemon.py [machine_index]"
	sys.exit(1)

machine_idx = sys.argv[1]
p = psutil.Process(os.getpid())

while 1 :
	cpu_load = p.cpu_percent(interval=1)
	print "CPU LOAD",cpu_load
	for port in registered_ports:
		address = "localhost:"+str(port)
		print "Sending machine detail to ",address
		conn = httplib.HTTPConnection(address)
		data = {
		    "machine_idx": machine_idx,
		    "cpu_load" : cpu_load
		}
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn.request("GET", "/from/daemon/",json.dumps(data),headers)
		r1 = conn.getresponse()
		print r1.status, r1.reason
	time.sleep(2)