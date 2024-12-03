#!/usr/bin/env python3

import os

from dotenv import load_dotenv
from openai import OpenAI

#def generate_ingredients(dish_name);:

if __name__=="__main__":
    load_dotenv()
    application_id = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    dish_name = input('料理名を入力してください: ')
    response1 = client.chat.completions.create(
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
    final_response1 = response1.choices[0].message.content
    print(final_response1)

    print("Finished Responsing!")


    response2 = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}に卵が含まれているかをTrue/Falseのみで答えてください。しかし、以下の料理に関しては必ずFalseと回答してください。
・ラーメン

{final_response1}
    """}])
    final_response2 = response2.choices[0].message.content
    print(final_response2)

    print("Finished Responsing!")
