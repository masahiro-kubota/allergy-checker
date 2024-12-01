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


if __name__ == '__main__':
    load_dotenv()
    application_id = os.getenv('RAKUTEN_API_APPLICATION_ID')
    #print("derive_category_list")
    #derive_category_list()
    #print("read_csv")
    recipe_df = pd.read_csv('data/category_list.csv')
    print("derive_recipe_id")
    cuisine_id = derive_recipe_id(recipe_df, "オムライス")
    # 「オムライス」カテゴリの人気レシピを取得
    print("derive_ingredients")
    ingredient_data = derive_ingredients(cuisine_id)
    #pprint(ingredient_data['result'][0]['recipeMaterial'])
    print(ingredient_data)







