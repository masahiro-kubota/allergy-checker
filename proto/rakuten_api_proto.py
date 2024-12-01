#!/usr/bin/env python

import json
import os
from pprint import pprint

from dotenv import load_dotenv
import pandas as pd
import requests



def derive_category_list():
    # レシピカテゴリー一覧を取得 https://webservice.rakuten.co.jp/documentation/recipe-category-list
    res = requests.get(f'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId={application_id}')
    json_data = json.loads(res.text)
    #pprint(json_data)

    row = []
    parent_dict = {}

    # 大カテゴリ
    for category in json_data['result']['large']:
        row.append({
            'category1': category['categoryId'],
            'category2': "",
            'category3': "",
            'categoryId': category['categoryId'],
            'categoryName': category['categoryName']
        })

    # 中カテゴリ
    for category in json_data['result']['medium']:
        row.append({
            'category1':category['parentCategoryId'],
            'category2':category['categoryId'],
            'category3':"",
            'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),
            'categoryName':category['categoryName']
        })
        parent_dict[str(category['categoryId'])] = category['parentCategoryId']

    # 小カテゴリ
    for category in json_data['result']['small']:
        row.append({'category1':parent_dict[category['parentCategoryId']],
                        'category2':category['parentCategoryId'],
                        'category3':category['categoryId'],
                        'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),
                        'categoryName':category['categoryName']
        })

    df = pd.DataFrame(row)
    df.to_csv('data/category_list.csv', index=True)
    #pprint(df)

def derive_recipe_id(df, recipe_name):
    df_querry = df.query(f'categoryName.str.contains("{recipe_name}")', engine='python')
    filtered_df = df_querry[df_querry['category3'].notna()]
    print(filtered_df)
    best_match_id = filtered_df.iloc[0]['categoryId']
    print(best_match_id)
    # TODO 小カテゴリまで含まれているもの。一致度が高いもの。
    return best_match_id

def derive_ingredients(recipe_id):
    # レシピIDからレシピ情報を取得 https://webservice.rakuten.co.jp/documentation/recipe-detail
    res = requests.get(f'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId={application_id}&categoryId={recipe_id}')
    json_data = json.loads(res.text)
    ingredient_list = []
    for i in json_data['result']:
        # TODO 重複を許しているので、重複を除去する
        ingredient_list.extend(i['recipeMaterial'])
    return ingredient_list

def check_allergens_in_recipe(recipe_database, recipe_name, allergens):
    ingredients = recipe_database.get(recipe_name)
    if not ingredients:
        return f"料理名 '{recipe_name}' のレシピが見つかりません。"
    detected_allergens = [a for a in allergens if any(a in i for i in ingredients)]

    return f"この料理にはアレルゲンが含まれています: {','.join(detected_allergens)}"

if __name__ == '__main__':
    load_dotenv()
    application_id = os.getenv('RAKUTEN_API_APPLICATION_ID')
    print("derive_category_list")
    derive_category_list()
    print("read_csv")
    recipe_df = pd.read_csv('data/category_list.csv')
    print("derive_recipe_id")
    cuisine_database = {}
    cuisine_name = "ソーセージ"
    cuisine_id = derive_recipe_id(recipe_df, cuisine_name)
    print("derive_ingredients")
    ingredient_data = derive_ingredients(cuisine_id)
    print(ingredient_data)
    cuisine_database[cuisine_name] = ingredient_data
    my_allergens = ["卵"]
    print(check_allergens_in_recipe(cuisine_database, cuisine_name, my_allergens))
    



# ベクトル検索を使う場合は、うまいことカテゴリーサイズを使えるかもしれない。

# TODO 卵の量を考慮したチェック（ドーナツ1個分ぐらいはいける）
# TODO 火が通ってるかどうかのチェック
# TODO マヨネーズ等卵が含まれた製品が弾けない。
# TODO 焼きそばと入力したとき、どの焼きそばか結構難しい
"""
      Unnamed: 0  category1  category2  category3   categoryId categoryName
913          913         16      155.0     1338.0  16-155-1338     あんかけ焼きそば
914          914         16      155.0      575.0   16-155-575        塩焼きそば
915          915         16      155.0      574.0   16-155-574      ソース焼きそば
916          916         16      155.0     2147.0  16-155-2147       かた焼きそば
918          918         16      155.0      152.0   16-155-152     アレンジ焼きそば
1243        1243         22      229.0     1017.0  22-229-1017       焼きそばパン
"""

# TODO ソーセージと検索したとき、添えられていると思われるジャガイモも原材料に含まれている。
"""
['ウィンナー', '卵', '★砂糖', '★塩', '☆ヤマサ昆布つゆ', '☆みりん', '☆醤油', 'マヨネーズ', 'ブラックペッパー', '乾燥パセリ', 'ウインナー', 'キャベツ', 'にんにく', 'バター', '塩こしょう', 'ウインナー', 'ジャガイモ', '玉ねぎ', '塩', 'こしょう', 'チーズ', 'あらびきソーセージ', '長芋', '★塩', '★粗挽き胡椒', '★にんにくチューブ']
この料理にはアレルゲンが含まれています: 卵
"""