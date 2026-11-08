import requests
import json

# Login with test user
url = "http://127.0.0.1:8000/api/v1/auth/login"
data = {"email": "testuser@example.com", "password": "testpass123"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)
token = response.json().get("access_token")
auth_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Add OpenRouter API key (test key)
print("Adding OpenRouter API key...")
key_data = {"provider": "openrouter", "api_key": "sk-or-v1-test1234567890"}
key_response = requests.post("http://127.0.0.1:8000/api/v1/auth/api-keys", json=key_data, headers=auth_headers)
print(f"Add Key Status: {key_response.status_code}")
print(f"Add Key Response: {key_response.json()}")

# List keys
keys_response = requests.get("http://127.0.0.1:8000/api/v1/auth/api-keys", headers=auth_headers)
print(f"\nList Keys Status: {keys_response.status_code}")
print(f"List Keys Response: {keys_response.json()}")

# Test model catalog with user key
catalog_response = requests.get("http://127.0.0.1:8000/api/v1/models/catalog", headers=auth_headers)
print(f"\nCatalog Status: {catalog_response.status_code}")
catalog = catalog_response.json()
for p in catalog['catalog']:
    if p['id'] == 'openrouter':
        available_count = sum(1 for m in p['models'] if m['available'])
        print(f"OpenRouter: has_key={p['has_api_key']}, models_available={available_count}")
        break

# Test chat with user key
chat_data = {"message": "merhaba", "agent_id": "main-manager"}
chat_response = requests.post("http://127.0.0.1:8000/api/v1/ai/chat", json=chat_data, headers=auth_headers)
print(f"\nChat Status: {chat_response.status_code}")
chat_result = chat_response.json()
print(f"Chat Response: {chat_result.get('response', '')[:100]}")
print(f"Provider: {chat_result.get('provider')}")
print(f"Model: {chat_result.get('model')}")

# Delete key
del_response = requests.delete("http://127.0.0.1:8000/api/v1/auth/api-keys/openrouter", headers=auth_headers)
print(f"\nDelete Key Status: {del_response.status_code}")
print(f"Delete Key Response: {del_response.json()}")

# List again
keys_response = requests.get("http://127.0.0.1:8000/api/v1/auth/api-keys", headers=auth_headers)
print(f"\nList Keys After Delete: {keys_response.json()}")