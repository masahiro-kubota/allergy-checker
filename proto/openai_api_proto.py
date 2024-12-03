#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from openai import OpenAI

def ask_dish_details(dish_name, client):
    
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": f"""
{dish_name}に関して以下の質問に回答してください。

原材料（10個）:
火が通っているかどうか：
1人前あたりに使用されている卵の量：
    """}],
      stream=False
    )
    final_response = response.choices[0].message.content
    return final_response

def check_ingredient(dish_name, ingredient, dish_details, client):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}に{ingredient}が含まれているかをTrue/Falseのみで答えてください。しかし、以下の料理に関しては必ずFalseと回答してください。
・ラーメン

{dish_details}
    """}])
    final_response = response.choices[0].message.content
    return final_response

if __name__=="__main__":
    load_dotenv()
    application_id = os.getenv('OPENAI_API_KEY')
    my_dish = input('料理名を入力してください: ')
    my_client = OpenAI()
    my_ingredient = "卵"
    my_dish_details = ask_dish_details(my_dish, my_client)
    print(my_dish_details)
    has_egg = check_ingredient(my_dish, my_ingredient, my_dish_details, my_client)
    print(has_egg)
    