import httplib, urllib
import json
import psutil,os
import sys
import time

class Daemon(BaseHTTPRequestHandler):
    # For Client Handling
    def do_POST(self):
        print "POST request"

    # For Each Node Communication
    def do_GET(self):
		p = psutil.virtual_memory()
		freeMemory = p.free
		print freeMemory
		self.wfile.write(str(freeMemory).encode('utf-8'))
		self.send_response(200)
		self.end_headers()

        except Exception as ex:
            self.send_response(500)
            self.end_headers()
            print(ex)

# Port ganti jadi yang bener
if len(sys.argv) < 2:
	print "Should be :"
	print "\t python daemon.py [port]"
	sys.exit(1)

server = HTTPServer(("", sys.argv[1]), Daemon)
server.serve_forever()
