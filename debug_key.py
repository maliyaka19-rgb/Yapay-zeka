import sys, os
sys.path.insert(0, r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
os.chdir(r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
from model_routes import _load_config, MODEL_CATALOG

config = _load_config()
print('Global config api_keys:', config.get('api_keys'))

provider_info = MODEL_CATALOG.get('openrouter')
print('OpenRouter env_key:', provider_info['env_key'])

env_val = os.getenv(provider_info['env_key'], '')
print(f'Env var value: "{env_val}"')
print(f'Env var length: {len(env_val)}')
print(f'_is_valid_key result: {env_val and len(env_val) >= 10 and not env_val.lower().startswith("your-") and not env_val.lower().startswith("sk-placeholder")}')