import requests
import json

# First try to register a new user to test
url = "http://127.0.0.1:8000/api/v1/auth/register"
data = {"email": "testuser@example.com", "username": "testuser", "password": "testpass123"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
print(f"Register Status: {response.status_code}")
print(f"Register Response: {response.json()}")

if response.status_code == 200:
    token = response.json().get("access_token")
    print(f"\nToken: {token[:50]}...")
    
    # Test /me endpoint
    me_headers = {"Authorization": f"Bearer {token}"}
    me_response = requests.get("http://127.0.0.1:8000/api/v1/auth/me", headers=me_headers)
    print(f"\nMe Status: {me_response.status_code}")
    print(f"Me Response: {me_response.json()}")
    
    # Test api-keys endpoint
    keys_response = requests.get("http://127.0.0.1:8000/api/v1/auth/api-keys", headers=me_headers)
    print(f"\nAPI Keys Status: {keys_response.status_code}")
    print(f"API Keys Response: {keys_response.json()}")
    
    # Test login with same credentials
    login_data = {"email": "testuser@example.com", "password": "testpass123"}
    login_response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json=login_data)
    print(f"\nLogin Status: {login_response.status_code}")
    print(f"Login Response: {login_response.json()}")