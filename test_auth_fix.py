import requests
import json

BASE = "http://127.0.0.1:8000"

print("=== TEST 1: Guest Login ===")
r = requests.post(f"{BASE}/api/v1/auth/guest", timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

if r.status_code == 200:
    token = r.json().get("access_token")
    print(f"Token: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test /me
    me = requests.get(f"{BASE}/api/v1/auth/me", headers=headers)
    print(f"\n/me Status: {me.status_code}")
    print(f"/me Response: {me.json()}")

print("\n=== TEST 2: Register New User ===")
reg_data = {"email": "testuser2@example.com", "username": "testuser2", "password": "testpass123"}
r = requests.post(f"{BASE}/api/v1/auth/register", json=reg_data, timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

if r.status_code == 200:
    token = r.json().get("access_token")
    print(f"Token: {token[:50]}...")

print("\n=== TEST 3: Login Existing User ===")
login_data = {"email": "testuser@example.com", "password": "testpass123"}
r = requests.post(f"{BASE}/api/v1/auth/login", json=login_data, timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

if r.status_code == 200:
    token = r.json().get("access_token")
    print(f"Token: {token[:50]}...")

print("\n=== TEST 4: Login Mali User ===")
login_data = {"email": "maliyaka19@gmail.com", "password": "test123"}
r = requests.post(f"{BASE}/api/v1/auth/login", json=login_data, timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")