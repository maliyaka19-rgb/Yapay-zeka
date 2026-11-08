import sys, os, asyncio
sys.path.insert(0, r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
os.chdir(r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
from ai_agent import get_agent_v6
from auth import auth_service
from model_routes import _load_config, _save_config, activate_model

async def test():
    agent = get_agent_v6()
    user = auth_service.get_user_by_email('maliyaka19@gmail.com')
    
    # Test 1: Current config (opencode) - should use opencode regardless of user keys
    agent._current_user = user
    agent._refresh_llm_config()
    print(f'Test 1 (opencode active): Provider={agent.provider}, Model={agent.llm_config.model}')
    
    # Test 2: Simulate openrouter active with user key
    # We'll manually set the config to openrouter and test
    config = _load_config()
    config['active_provider'] = 'openrouter'
    config['active_model'] = 'meta-llama/llama-3.1-70b-instruct:free'
    _save_config(config)
    
    # Refresh agent config
    agent._current_user = user
    agent._refresh_llm_config()
    print(f'Test 2 (openrouter + user key): Provider={agent.provider}, Model={agent.llm_config.model}, API Key set={bool(agent.llm_config.api_key)}, Key preview={agent.llm_config.api_key[:20] if agent.llm_config.api_key else "None"}')
    
    # Test 3: Without user (should fall back to global config which has no key)
    agent._current_user = None
    agent._refresh_llm_config()
    print(f'Test 3 (openrouter no user): Provider={agent.provider}, Model={agent.llm_config.model}, API Key set={bool(agent.llm_config.api_key)}')
    
    # Restore opencode
    config = _load_config()
    config['active_provider'] = 'opencode'
    config['active_model'] = 'deepseek-v4.1-flash-free'
    _save_config(config)
    agent._refresh_llm_config()
    print(f'Test 4 (restored opencode): Provider={agent.provider}, Model={agent.llm_config.model}')

asyncio.run(test())