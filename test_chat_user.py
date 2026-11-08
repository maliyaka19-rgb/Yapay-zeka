import sys, os, asyncio
sys.path.insert(0, r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
os.chdir(r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
from ai_agent import chat
from auth import auth_service
from model_routes import _load_config, _save_config

async def test():
    user = auth_service.get_user_by_email('maliyaka19@gmail.com')
    # Switch to openrouter temporarily
    config = _load_config()
    config['active_provider'] = 'openrouter'
    config['active_model'] = 'meta-llama/llama-3.1-70b-instruct:free'
    _save_config(config)
    
    result = await chat('merhaba', current_user=user)
    print('Success:', result.get('success'))
    print('Response:', result.get('response', '')[:100])
    print('Provider:', result.get('provider'))
    print('Model:', result.get('model'))
    
    # Restore
    config = _load_config()
    config['active_provider'] = 'opencode'
    config['active_model'] = 'deepseek-v4.1-flash-free'
    _save_config(config)

asyncio.run(test())