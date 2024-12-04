import asyncio
import json
import time
from time import time, sleep

from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv
from quart import Quart, request, jsonify, Response
from quart_cors import cors
from openai import AsyncOpenAI



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

#def check_eatable(results):
    

async def async_main(my_dish):
    async_client = AsyncOpenAI()
    start_time = time()

    task1_1 = asyncio.create_task(ask_dish_details_async(my_dish, async_client, start_time))
    task1_2 = asyncio.create_task(check_white_list_dish_async(my_dish, "ラーメン", async_client, 3, start_time))
    task1 = [task1_1, task1_2]
    results1 = await asyncio.gather(*task1)
    # TODO 原材料と火が通っているかの確認は並行して処理できるからここでgatherする必要がない。

    my_dish_details = results1[0]
    check_white_list_dishes = results1[1]
    print(my_dish_details)
    task2_1 = asyncio.create_task(check_ingredient_async(my_dish, "卵", my_dish_details, async_client, 1, start_time))
    task2_2 = asyncio.create_task(check_ingredient_async(my_dish, "芋類", my_dish_details, async_client, 1, start_time))
    task2_3 = asyncio.create_task(check_ingredient_async(my_dish, "生野菜", my_dish_details, async_client, 1, start_time))
    #task2_3 = asyncio.create_task(check_white_list_async(my_dish, "ラーメン", async_client, 3, start_time))
    # TODO 原材料確認と火が通っているかの確認は別で動かした方が速い。
    # TODO 追加確認材料 いも類　ナッツ類　甲殻類　貝類　ごぼう　れんこん　こんにゃく　そば　生野菜・生肉・生魚
    # 追加ホワイトリスト　卵（ラーメン）　イモ類（さつまいも）　果物（柑橘類　いちご　ぶどう　パイナップル　りんご　缶詰）豆（醤油　味噌）　甲殻類（えびせん　桜えび）　　
    tasks2 = [task2_1, task2_2, task2_3]
    results2 = await asyncio.gather(*tasks2)
    check_egg = results2[0]
    check_potato = results2[1]
    check_raw_vegetable = results2[2]
    print(results2[0])
    safe_to_eat = check_white_list_dishes or (check_egg and check_potato and check_raw_vegetable)
    elements_dict = {
    "check_white_list_dishes": check_white_list_dishes,
    "check_egg": check_egg,
    "check_potato": check_potato,
    "check_raw_vegetable": check_raw_vegetable,
    "safe_to_eat": safe_to_eat
    }
    return elements_dict

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
        yield json.dumps({key: result}, ensure_ascii=False) + "\n"  # 日本語をエスケープしない
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
        yield json.dumps({key: result}) + "\n"
    final_answer = my_dict["white_list_tf"] or (my_dict["ingredient_tf"] and my_dict["cooked_tf"])
    yield json.dumps({"final_answer": final_answer}, ensure_ascii=False) + "\n"  # 日本語をエスケープしない


def generate_responses():
    messages = ["Task 1 completed", "Task 2 completed", "Task 3 completed"]
    for message in messages:
        yield f"data: {message}\n\n"  # SSE形式でデータを送信
        sleep(1)  # タスク間で擬似的に遅延を追加（デモ用）


def create_app():
    my_app = Quart(__name__)
    
    cors(my_app, allow_origin="*")
    @my_app.route('/check_allergy', methods=['POST'])
    def check_allergy():
        try:
            # リクエストからデータを取得
            data = request.get_json()
            dish_name = data.get('dish_name')
            load_dotenv()
            result_dict = asyncio.run(async_main(dish_name))
            answer = result_dict["safe_to_eat"]
            print("answer", answer)
            if answer:
                print(f"{dish_name}は食べられます。")
            else:
                print(f"{dish_name}は食べられません。")

            return jsonify(result_dict)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @my_app.route('/stream', methods=['GET'])
    def stream():
        # レスポンスをSSE形式にして返す
        return Response(generate_responses(), content_type='text/event-stream')

    @my_app.route('/check_allergy_stream', methods=['POST'])
    async def check_allergy_stream():
        data = await request.get_json()
        dish_name = data.get("dish_name")
        load_dotenv()
        if not dish_name:
            return jsonify({"error": "Dish name is required"}), 400
        # SSEでレスポンスをストリームとして返す
        return Response(async_create_tasks(dish_name), mimetype='text/event-stream')


    return my_app

app = create_app()

