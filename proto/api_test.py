import requests
import json
import os
from pprint import pprint

from dotenv import load_dotenv

load_dotenv()
application_id = os.getenv("RAKUTEN_API_APPLICATION_ID")

# レシピカテゴリー一覧を取得 https://webservice.rakuten.co.jp/documentation/recipe-category-list
res = requests.get(f'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId={application_id}')
json_data = json.loads(res.text)
pprint(json_data)