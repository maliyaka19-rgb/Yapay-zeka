import requests

r = requests.get('http://127.0.0.1:8000/', timeout=5)
print('Status:', r.status_code)
print('Content-Type:', r.headers.get('content-type'))
print('Length:', len(r.text))
print(r.text[:500])