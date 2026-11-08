import requests
import json

BASE = "http://127.0.0.1:8000"

print("=== FULL FLOW TEST ===\n")

# 1. Guest login
print("1. GUEST LOGIN")
r = requests.post(f"{BASE}/api/v1/auth/guest", timeout=10)
print(f"   Status: {r.status_code}")
guest_token = r.json().get("access_token")
print(f"   Token: {guest_token[:30]}...")

headers = {"Authorization": f"Bearer {guest_token}"}

# 2. Check /me
print("\n2. /me WITH GUEST TOKEN")
r = requests.get(f"{BASE}/api/v1/auth/me", headers={"Authorization": f"Bearer {guest_token}"})
print(f"   Status: {r.status_code}")
print(f"   User: {r.json().get('username')}")

# 3. Model catalog with guest
print("\n3. MODEL CATALOG (GUEST)")
r = requests.get(f"{BASE}/api/v1/models/catalog", headers=headers)
print(f"   Status: {r.status_code}")
catalog = r.json()
for p in catalog['catalog']:
    if p['id'] in ['opencode', 'local']:
        print(f"   {p['id']}: available={p['available']}")

# 4. Chat with guest
print("\n4. CHAT (GUEST)")
r = requests.post(f"{BASE}/api/v1/ai/chat", 
    json={"message": "merhaba", "agent_id": "main-manager"}, 
    headers=headers, timeout=30)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   Response: {r.json().get('response', '')[:80]}")
    print(f"   Provider: {r.json().get('provider')}")

# 5. Register new user
print("\n5. REGISTER NEW USER")
reg_data = {"email": "flowtest@example.com", "username": "flowtest", "password": "test123"}
r = requests.post(f"{BASE}/api/v1/auth/register", json=reg_data)
print(f"   Status: {r.status_code}")
user_token = r.json().get("access_token")
print(f"   Token: {user_token[:30]}...")

# 6. Model catalog with user
print("\n6. MODEL CATALOG (USER)")
user_headers = {"Authorization": f"Bearer {user_token}"}
r = requests.get(f"{BASE}/api/v1/models/catalog", headers=user_headers)
print(f"   Status: {r.status_code}")

# 7. Add API key
print("\n7. ADD API KEY")
r = requests.post(f"{BASE}/api/v1/auth/api-keys", 
    json={"provider": "openrouter", "api_key": "sk-or-v1-test1234567890"},
    headers=user_headers)
print(f"   Status: {r.status_code}")

# 8. List keys
print("\n8. LIST API KEYS")
r = requests.get(f"{BASE}/api/v1/auth/api-keys", headers=user_headers)
print(f"   Status: {r.status_code}")
print(f"   Keys: {r.json()}")

# 9. Chat with user (with key)
print("\n9. CHAT (USER WITH KEY)")
r = requests.post(f"{BASE}/api/v1/ai/chat",
    json={"message": "merhaba", "agent_id": "main-manager"},
    headers=user_headers, timeout=30)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    print(f"   Provider: {r.json().get('provider')}")

# 10. Login existing user
print("\n10. LOGIN EXISTING USER")
r = requests.post(f"{BASE}/api/v1/auth/login", 
    json={"email": "testuser@example.com", "password": "testpass123"})
print(f"   Status: {r.status_code}")

print("\n=== ALL TESTS COMPLETE ===")