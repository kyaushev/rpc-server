import json
import requests

rpc_command = json.dumps({ "id": 1, "func": "getNews", "args": ["2022-09-11", "2022-09-14"] })
print(rpc_command)
r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
rpc_resp = r.json()
print(r.status_code, rpc_resp)