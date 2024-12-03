#!/usr/bin/env python3
import asyncio
import os
from time import time

from dotenv import load_dotenv
from openai import AsyncOpenAI,OpenAI

def ask_dish_details(dish_name, client, start_time):
    
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
    end = time()
    elapsed_time = end - start_time
    print(f"Task finished in {elapsed_time} seconds")
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



async def check_ingredient_async(dish_name, ingredient, dish_details, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}に{ingredient}が含まれているかをTrue/Falseのみで答えてください。しかし、以下の料理に関しては必ずFalseと回答してください。
・ラーメン

{dish_details}
    """}])
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds")
    print(final_response)
    return final_response

async def async_main(start_time):
    async_client = AsyncOpenAI()
    client = OpenAI()
    my_dish = input('料理名を入力してください: ')
    my_dish_details = ask_dish_details(my_dish, client, start_time)
    print(my_dish_details)
    task1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", my_dish_details, async_client, 1, start_time))
    task2 = asyncio.create_task(check_ingredient_async(my_dish, "豚肉", my_dish_details, async_client, 2, start_time))
    task3 = asyncio.create_task(check_ingredient_async(my_dish, "牛乳", my_dish_details, async_client, 3, start_time))
    tasks = [task1, task2, task3]
    await asyncio.gather(*tasks)

#TODO Trueが含まれているかFalseが含まれているかで後処理する。Trueの方が多かったらTrueにしてしまう。Trueだけを出力しなかった場合記録するか。
"""
卵が含まれているかをTrue/Falseのみで答えてください。
- 牛丼：True

"""

if __name__=="__main__":
    my_start_time = time()
    
    
    load_dotenv()
    #my_dish = input('料理名を入力してください: ')
    my_async_client = AsyncOpenAI()
    my_clinet = OpenAI()
    asyncio.run(async_main(my_start_time))
    """
    my_ingredient = "卵"
    my_dish_details = ask_dish_details(my_dish, my_client)
    print(my_dish_details)
    has_egg = check_ingredient(my_dish, my_ingredient, my_dish_details, my_client)
    print(has_egg)
    """
    