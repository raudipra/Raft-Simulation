'''
import httplib
conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason

data1 = r1.read()
conn.request("GET", "/parrot.spam")
r2 = conn.getresponse()
print r2.status, r2.reason
Not Found
data2 = r2.read()
conn.close()
'''

import httplib, urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:10001")
conn.request("POST", "/", params, headers)
response = conn.getresponse()
print response.status, response.reason

data = response.read()
conn.close()
