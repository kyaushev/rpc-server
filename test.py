import json
import requests

# rpc_command = json.dumps({ "id": 1, "func": "addNews", "args": ["Новость", "Был создан дамп", "2022-09-11"] })
# print(rpc_command)
# r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
# rpc_resp = r.json()
# print(r.status_code, rpc_resp)

rpc_command = json.dumps({ "id": 1, "func": "updateNews", "args": [8,  "Новость", "DATA updated", "2022-09-11"] })
print(rpc_command)
r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
rpc_resp = r.json()
print(r.status_code, rpc_resp)

rpc_command = json.dumps({ "id": 2, "func": "getNews", "args": ["2022-09-11", "2022-09-14"] })
print(rpc_command)
r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
rpc_resp = r.json()
print(r.status_code, rpc_resp)

rpc_command = json.dumps({ "id": 3, "func": "deleteNews", "args": [1] })
print(rpc_command)
r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
rpc_resp = r.json()
print(r.status_code, rpc_resp)

rpc_command = json.dumps({ "id": 4, "func": "getNews", "args": ["2022-09-11", "2022-09-14"] })
print(rpc_command)
r = requests.post("http://127.0.0.1:5000/api/v1/rpc", json=rpc_command)
rpc_resp = r.json()
print(r.status_code, rpc_resp)