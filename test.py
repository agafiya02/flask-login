import requests

print(requests.get('http://127.0.0.1:5000/api/v2/users').json())
print(requests.get('http://localhost:5000/api/v2/1').json())
print(requests.get('http://localhost:5000/api/v2/kkhf').json())
