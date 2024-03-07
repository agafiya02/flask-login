import requests

print(requests.get('http://127.0.0.1:5000/api/jobs').json())
print(requests.get('http://localhost:5000/api/jobs/1').json())
print(requests.get('http://localhost:5000/api/jobs/528').json())
print(requests.get('http://localhost:5000/api/jobs/ij').json())
