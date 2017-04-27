# # import jsox`n
# import requests
# payload = {'key1': 'value1', 'key2': 'value2'}
# # data_json = json.dumps(data)
# # payload = {'json_payload': data_json, 'apikey': 'YOUR_API_KEY_HERE'}
# r = requests.get('http://localhost:13337/1/2', data=payload)
# print(r.status_code, r.reason)

import httplib, urllib
import json
# params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
conn = httplib.HTTPConnection("localhost:13337")
data = {
    "address": "localhost",
    "port": "12345",
    "cpu_load": "1000" 
}
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn.request("GET", "/",json.dumps(data),headers)
r1 = conn.getresponse()
print r1.status, r1.reason