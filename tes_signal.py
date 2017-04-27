import signal

def handler(signum, frame):
	print "Forever is over!"
	signal.alarm(3)
	loop_forever()
	raise Exception("end of time") 

# This function *may* run for an indetermined time...
def loop_forever():
    import time
    a = 1
    while 1:
        print "sec"
        time.sleep(1)
        a += 1
        if (a == 5):
        	signal.alarm(1) 

# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

# Define a timeout for your function
signal.alarm(10)

try:
    loop_forever()
except Exception, exc: 
    print exc