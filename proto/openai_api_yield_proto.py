#!/usr/bin/env python3
import asyncio
import os
from time import time

from dotenv import load_dotenv
from openai import AsyncOpenAI,OpenAI


async def ask_dish_details_async(dish_name, client, start_time):
    
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}に関して以下の質問に回答してください。

原材料（10個）:
    """}],
      stream=False
    )
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"Task 1 finished in {elapsed_time} seconds")
    key = "dish_details"
    return key, final_response

async def ask_dish_cooked_async(dish_name, client, start_time):
    
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}に関して以下の質問に回答してください。

火が通っているかどうか：
    """}],
      stream=False
    )
    final_response = response.choices[0].message.content
    print(final_response)
    end = time()
    elapsed_time = end - start_time
    print(f"Task 2 finished in {elapsed_time} seconds")
    key = "cooked"
    return key, final_response


async def check_ingredient_async(dish_name, ingredient, dish_details, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}に{ingredient}が含まれているかをTrue/Falseのみで答えてください。

{dish_details}
    """}])
    llm_response = response.choices[0].message.content
    final_response = not check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    key = "ingredient_tf"
    return key, final_response

async def check_cooked_async(dish_name, dish_details, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
以下を参考にして、{dish_name}は火が通っているかをTrue/Falseのみで答えてください。

{dish_details}
    """}])
    llm_response = response.choices[0].message.content
    final_response = check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    key = "cooked_tf"
    return key, final_response

async def check_white_list_dish_async(dish_name, white_list, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}は以下の料理に含まれるかをTrue/Falseのみで答えてください。

{white_list}
    """}])
    llm_response = response.choices[0].message.content
    final_response = check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    key = "white_list_tf"
    return key, final_response


def check_true_false(response):
    true_num  = response.count("True")
    false_num = response.count("False")
    return true_num > false_num


async def async_create_tasks(my_dish):
    async_client = AsyncOpenAI()
    start_time = time()
    my_dict = {}
    task1_1 = asyncio.create_task(ask_dish_details_async(my_dish, async_client, start_time))
    task1_2 = asyncio.create_task(ask_dish_cooked_async(my_dish, async_client, start_time))
    task1_3 = asyncio.create_task(check_white_list_dish_async(my_dish, "ラーメン", async_client, 3, start_time))
    task1 = [task1_1, task1_2, task1_3]
    for completed_task in asyncio.as_completed(task1):
        key, result = await completed_task
        my_dict[key] = result
        yield key, result
    print(my_dict)
    #results1 = await asyncio.gather(*task1)
    # TODO 原材料と火が通っているかの確認は並行して処理できるからここでgatherする必要がない。

    my_dish_details = my_dict["dish_details"]
    my_details_cooked = my_dict["cooked"]
    print(my_dish_details)
    task2_1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", my_dish_details, async_client, 1, start_time))
    task2_2 = asyncio.create_task(check_cooked_async(my_dish, my_details_cooked, async_client, 2, start_time))
    #task2_3 = asyncio.create_task(check_white_list_async(my_dish, "ラーメン", async_client, 3, start_time))
    # TODO 原材料確認と火が通っているかの確認は別で動かした方が速い。
    # TODO 追加確認材料 いも類　ナッツ類　甲殻類　貝類　ごぼう　れんこん　こんにゃく　そば　
    # 追加ホワイトリスト　卵（ラーメン）　イモ類（さつまいも）　果物（柑橘類　いちご　ぶどう　パイナップル　りんご　缶詰）豆（醤油　味噌）　甲殻類（えびせん　桜えび）　　
    tasks2 = [task2_1, task2_2]
    for completed_task in asyncio.as_completed(tasks2):
        key, result = await completed_task
        my_dict[key] = result
        yield key, result
    final_answer = my_dict["white_list_tf"] or (my_dict["ingredient_tf"] and my_dict["cooked_tf"])
    yield "final_answer", final_answer



async def async_main(my_dish):
    response_dict = {}
    async for key, result in async_create_tasks(my_dish):
        response_dict[key] = result
    return response_dict

if __name__=="__main__":
    load_dotenv()
    dish = input('料理名を入力してください: ')
    answer = asyncio.run(async_main(dish))
    print("answer", answer)
    if answer["final_answer"]:
        print(f"{dish}は食べられます。")
    else:
        print(f"{dish}は食べられません。")
    

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