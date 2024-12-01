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
    # TODO 小カテゴリまで含まれているもの。一致度が高いもの。
    recipe_id = "14-121-553"
    return recipe_id

def derive_ingredients(recipe_id):
    # レシピIDからレシピ情報を取得 https://webservice.rakuten.co.jp/documentation/recipe-detail
    res = requests.get(f'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId={application_id}&categoryId={recipe_id}')
    json_data = json.loads(res.text)
    ingredient_list = []
    for i in json_data['result']:
        ingredient_list.extend(i['recipeMaterial'])
    return ingredient_list

def check_allergens_in_recipe(recipe_database, recipe_name, allergens):
    ingredients = recipe_database.get(recipe_name)
    if not ingredients:
        return f"料理名 '{recipe_name}' のレシピが見つかりません。"
    # 原材料の中にアレルゲンが含まれているかチェック
    """
    detected_allergens = []
    for i in ingredients:
        for a in allergens:
            if a in i:
                detected_allergens.append(a)
    """
    
    detected_allergens = [a for a in allergens if any(a in i for i in ingredients)]

    return f"この料理にはアレルゲンが含まれています: {','.join(detected_allergens)}"

if __name__ == '__main__':
    load_dotenv()
    application_id = os.getenv('RAKUTEN_API_APPLICATION_ID')
    #print("derive_category_list")
    #derive_category_list()
    #print("read_csv")
    recipe_df = pd.read_csv('data/category_list.csv')
    print("derive_recipe_id")
    cuisine_database = {}
    cuisine_name = "オムライス"
    cuisine_id = derive_recipe_id(recipe_df, cuisine_name)
    # 「オムライス」カテゴリの人気レシピを取得
    print("derive_ingredients")
    ingredient_data = derive_ingredients(cuisine_id)
    #print(ingredient_data)
    cuisine_database["オムライス"] = ingredient_data
    my_allergens = ["卵", "豆"]
    print(check_allergens_in_recipe(cuisine_database, cuisine_name, my_allergens))
    







