import requests

mydata = [
    {"id": 1, "name": "alice", "category": "A", "sub_category": "X"},
    {"id": 2, "name": "Bob", "category": "B", "sub_category": "Y"}, 
    {"id": 3, "name": "Charlie", "category": "A", "sub_category": "Z"},
    {"id": 4, "name": "David", "category": "B", "sub_category": "X"}
]

headers = {'Content-Type': 'application/json'}
req = requests.post("http://127.0.0.1:5001/parsing", json=mydata, headers=headers)

# Menampilkan hasil request
print("Status Code:", req.status_code)
print("Response:", req.text)
