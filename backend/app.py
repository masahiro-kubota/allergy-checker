import asyncio
import os
from time import time

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from openai import AsyncOpenAI,OpenAI


app = Flask(__name__)

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
    print(f"Task 2 finished in {elapsed_time} seconds")
    return final_response

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
    print(f"Task 3 finished in {elapsed_time} seconds")
    return final_response


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
    return final_response

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
    return final_response

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
    return final_response


def check_true_false(response):
    true_num  = response.count("True")
    false_num = response.count("False")
    return true_num > false_num

#def check_eatable(results):
    

async def async_main(my_dish):
    async_client = AsyncOpenAI()
    start_time = time()

    task1_1 = asyncio.create_task(ask_dish_details_async(my_dish, async_client, start_time))
    task1_2 = asyncio.create_task(ask_dish_cooked_async(my_dish, async_client, start_time))
    task1_3 = asyncio.create_task(check_white_list_dish_async(my_dish, "ラーメン", async_client, 3, start_time))
    task1 = [task1_1, task1_2, task1_3]
    results1 = await asyncio.gather(*task1)
    # TODO 原材料と火が通っているかの確認は並行して処理できるからここでgatherする必要がない。

    my_dish_details = results1[0]
    my_details_cooked = results1[1]
    check_white_list_dishes = results1[2]
    print(my_dish_details)
    task2_1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", my_dish_details, async_client, 1, start_time))
    task2_2 = asyncio.create_task(check_cooked_async(my_dish, my_details_cooked, async_client, 2, start_time))
    #task2_3 = asyncio.create_task(check_white_list_async(my_dish, "ラーメン", async_client, 3, start_time))
    # TODO 原材料確認と火が通っているかの確認は別で動かした方が速い。
    # TODO 追加確認材料 いも類　ナッツ類　甲殻類　貝類　ごぼう　れんこん　こんにゃく　そば　
    # 追加ホワイトリスト　卵（ラーメン）　イモ類（さつまいも）　果物（柑橘類　いちご　ぶどう　パイナップル　りんご　缶詰）豆（醤油　味噌）　甲殻類（えびせん　桜えび）　　
    tasks2 = [task2_1, task2_2]
    results2 = await asyncio.gather(*tasks2)
    check_egg = results2[0]
    check_cooked = results2[1]
    print(results2[0])
    final_answer = check_white_list_dishes or (check_egg and check_cooked)
    return final_answer


@app.route('/check_allergy', methods=['POST'])
def check_allergy():
    try:
        # リクエストからデータを取得
        data = request.get_json()
        dish_name = data.get('dish_name')
        load_dotenv()
        answer = asyncio.run(async_main(dish_name))
        print("answer", answer)
        if answer:
            print(f"{dish_name}は食べられます。")
        else:
            print(f"{dish_name}は食べられません。")

        return jsonify({"safe_to_eat": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)
