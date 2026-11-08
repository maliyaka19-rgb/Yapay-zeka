import sys, os, asyncio
sys.path.insert(0, r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
os.chdir(r'C:\Users\HP\Desktop\YAPAY ZEKA\multimodal-studio\backend')
from model_routes import get_model_catalog
from auth import auth_service

async def test():
    user = auth_service.get_user_by_email('maliyaka19@gmail.com')
    catalog = await get_model_catalog(current_user=user)
    print('Catalog providers:')
    for p in catalog['catalog']:
        available_count = sum(1 for m in p['models'] if m['available'])
        print(f'  {p["id"]}: has_key={p["has_api_key"]}, models_available={available_count}')
    print(f'Active: {catalog["active_provider"]}/{catalog["active_model"]}')

asyncio.run(test())