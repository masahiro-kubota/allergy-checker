import asyncio
import json
import time
from time import time, sleep

from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv
from quart import Quart, request, jsonify, Response
from quart_cors import cors
from openai import AsyncOpenAI


# Not used now
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


# Not used now
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


async def check_ingredient_async(dish_name, ingredient, ingredient_key, dish_details, client, num, start_time):
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
    key = ingredient_key + "_tf"
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



async def create_tasks_async(my_dish):
    async_client = AsyncOpenAI()
    start_time = time()
    my_dict = {}
    task1_1 = asyncio.create_task(ask_dish_details_async(my_dish, async_client, start_time))
    task1_2 = asyncio.create_task(check_white_list_dish_async(my_dish, "ラーメン", async_client, 3, start_time))
    task1 = [task1_1, task1_2]
    for completed_task in asyncio.as_completed(task1):
        key, result = await completed_task
        my_dict[key] = result
        yield f"data: {json.dumps({'type': key, 'result': result}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない

    print(my_dict)
    #results1 = await asyncio.gather(*task1)
    # TODO 原材料と火が通っているかの確認は並行して処理できるからここでgatherする必要がない。

    my_dish_details = my_dict["dish_details"]
    print(my_dish_details)
    task2_1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", "egg", my_dish_details, async_client, 1, start_time))
    task2_2 = asyncio.create_task(check_ingredient_async(my_dish, "さつまいも以外の芋類", "potato", my_dish_details, async_client, 1, start_time))
    task2_3 = asyncio.create_task(check_ingredient_async(my_dish, "加熱処理されていない野菜", "raw_vegetables", my_dish_details, async_client, 1, start_time))
    task2_4 = asyncio.create_task(check_ingredient_async(my_dish, "ナッツ", "nuts", my_dish_details, async_client, 1, start_time))
    task2_5 = asyncio.create_task(check_ingredient_async(my_dish, "ごぼう", "burdock", my_dish_details, async_client, 1, start_time))
    task2_6 = asyncio.create_task(check_ingredient_async(my_dish, "れんこん", "lotus", my_dish_details, async_client, 1, start_time))
    task2_7 = asyncio.create_task(check_ingredient_async(my_dish, "こんにゃく", "konjac", my_dish_details, async_client, 1, start_time))
    task2_8 = asyncio.create_task(check_ingredient_async(my_dish, "そば", "buckwheat", my_dish_details, async_client, 1, start_time))
    #task2_3 = asyncio.create_task(check_white_list_async(my_dish, "ラーメン", async_client, 3, start_time))
    # TODO 追加確認材料 ナッツ類　甲殻類　ごぼう　れんこん　こんにゃく　そば　
    # 追加ホワイトリスト　卵（ラーメン）　イモ類（さつまいも）　果物（柑橘類　いちご　ぶどう　パイナップル　りんご　缶詰）豆（醤油　味噌）　甲殻類（えびせん　桜えび）　　
    tasks2 = [task2_1, task2_2, task2_3, task2_4, task2_5, task2_6, task2_7, task2_8]
    for completed_task in asyncio.as_completed(tasks2):
        key, result = await completed_task
        my_dict[key] = result
        yield f"data: {json.dumps({'type': key, 'result': result}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない
    result = my_dict["white_list_tf"] or (my_dict["egg_tf"] and my_dict["potato_tf"] and my_dict["raw_vegetables_tf"] and my_dict["nuts_tf"] and my_dict["burdock_tf"] and my_dict["lotus_tf"] and my_dict["Konjac_tf"] and my_dict["buckwheat_tf"])
    yield f"data: {json.dumps({'type': 'safe_to_eat', 'result': result}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない


def generate_responses():
    messages = ["Task 1 completed", "Task 2 completed", "Task 3 completed"]
    for message in messages:
        yield f"data: {message}\n\n"  # SSE形式でデータを送信
        sleep(1)  # タスク間で擬似的に遅延を追加（デモ用）


def create_app():
    my_app = Quart(__name__)
    
    cors(my_app, allow_origin="*")

    @my_app.route('/stream', methods=['GET'])
    def stream():
        # レスポンスをSSE形式にして返す
        return Response(generate_responses(), content_type='text/event-stream')

    @my_app.route('/check_allergy_stream', methods=['GET'])
    async def check_allergy_stream():
        # クエリパラメータから "dish_name" を取得
        dish_name = request.args.get("dish_name")  # GET リクエストでは request.args を使用
        load_dotenv()
        if not dish_name:
            return jsonify({"error": "Dish name is required"}), 400

        async def stream():
            async for chunk in create_tasks_async(dish_name):
                yield chunk.encode("utf-8")  # UTF-8 にエンコード

        return Response(stream(), mimetype='text/event-stream')



    return my_app

app = create_app()

