#!/usr/bin/env python3
import asyncio
import os
from time import time

from dotenv import load_dotenv
from openai import AsyncOpenAI,OpenAI

def ask_dish_details(dish_name, client, start_time):
    
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}に関して以下の質問に回答してください。

原材料（10個）:
火が通っているかどうか：
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
      model="gpt-4o-mini",
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
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}に{ingredient}が含まれているかをTrue/Falseのみで答えてください。

{dish_details}
    """}])
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    return final_response

async def check_cooked_async(dish_name, dish_details, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}は火が通っているかをTrue/Falseのみで答えてください。

{dish_details}
    """}])
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    return final_response

async def check_white_list_async(dish_name, white_list, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}は以下の料理に含まれるかをTrue/Falseのみで答えてください。

{white_list}
    """}])
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    return final_response

async def async_main():
    async_client = AsyncOpenAI()
    client = OpenAI()
    my_dish = input('料理名を入力してください: ')
    start_time = time()
    my_dish_details = ask_dish_details(my_dish, client, start_time)
    print(my_dish_details)
    task1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", my_dish_details, async_client, 1, start_time))
    task2 = asyncio.create_task(check_cooked_async(my_dish, my_dish_details, async_client, 2, start_time))
    task3 = asyncio.create_task(check_white_list_async(my_dish, "ラーメン", async_client, 3, start_time))
    # TODO 回答している時間が長いから、回答が短くなるように質問を分けたほうがいい。
    # TODO 原材料確認と火が通っているかの確認は別で動かした方が速い。
    # TODO 追加確認材料 いも類　ナッツ類　甲殻類　貝類　ごぼう　れんこん　こんにゃく　そば　
    # 追加ホワイトリスト　卵（ラーメン）　イモ類（さつまいも）　果物（柑橘類　いちご　ぶどう　パイナップル　りんご　缶詰）豆（醤油　味噌）　甲殻類（えびせん　桜えび）　　
    tasks = [task1, task2, task3]
    await asyncio.gather(*tasks)



if __name__=="__main__":
    
    
    
    load_dotenv()
    #my_dish = input('料理名を入力してください: ')
    my_async_client = AsyncOpenAI()
    my_clinet = OpenAI()
    asyncio.run(async_main())
    """
    my_ingredient = "卵"
    my_dish_details = ask_dish_details(my_dish, my_client)
    print(my_dish_details)
    has_egg = check_ingredient(my_dish, my_ingredient, my_dish_details, my_client)
    print(has_egg)
    """
    

#TODO Trueが含まれているかFalseが含まれているかで後処理する。Trueの方が多かったらTrueにしてしまう。Trueだけを出力しなかった場合記録するか。
"""
卵が含まれているかをTrue/Falseのみで答えてください。
- 牛丼：True

"""