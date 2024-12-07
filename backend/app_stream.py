import asyncio
import json
import time
from time import time, sleep

from dotenv import load_dotenv
import sqlite3
from quart import Quart, request, jsonify, Response, render_template
from quart_cors import cors
from openai import AsyncOpenAI
import yaml

import os


async def ask_dish_or_ingredient_coro(name, client, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{name}は料理ですか？True/Falseのみで答えてください。"""}])
    llm_response = response.choices[0].message.content
    final_response = check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"ask_dish_or_ingredient_async finished in {elapsed_time} seconds: {final_response}")
    key = "dish_tf"
    reason = None
    return key, final_response, reason

# 料理の作り方を確認
async def ask_dish_details_coro(dish_name, client, start_time):
    
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}を作る手順を簡潔に教えてください。
    """}],
      stream=False
    )
    final_response = response.choices[0].message.content
    end = time()
    elapsed_time = end - start_time
    print(f"ask_dish_details_async finished in {elapsed_time} seconds")
    key = "dish_details"
    return key, final_response

# 料理の手順を確認


async def check_ingredient_coro(dish_name, ingredient, ingredient_key, data_dict, client, num, start_time):
    if data_dict["dish_tf"]:
        prompt = f"""
以下を参考にして、{dish_name}に{ingredient}が含まれているかをTrue/Falseのみで答えてください。

{data_dict['dish_details']}
    """
    else:
        prompt = f"""
以下を参考にして、{dish_name}は{ingredient}であるかをTrue/Falseのみで答えてください。
"""
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": prompt}])
    llm_response = response.choices[0].message.content
    final_response = not check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"Task {num} finished in {elapsed_time} seconds: {final_response}")
    key = ingredient_key + "_tf"
    return key, final_response


async def check_white_list_dish_coro(dish_name, white_list, white_list_key, reason, client, num, start_time):
    response = await client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": f"""
{dish_name}は{white_list}ですか？True/Falseのみで答えてください。
    """}])
    llm_response = response.choices[0].message.content
    final_response = check_true_false(llm_response)
    end = time()
    elapsed_time = end - start_time
    print(f"check_white_list_dish_async {num} finished in {elapsed_time} seconds: {final_response}")
    key = white_list_key + "_tf"
    if not final_response:
        reason = None
    return key, final_response, reason


def check_true_false(response):
    true_num  = response.count("True")
    false_num = response.count("False")
    return true_num > false_num



async def create_tasks_coro(my_dish):
    async_client = AsyncOpenAI()
    start_time = time()
    my_dict = {}
    my_dict["reason"] = None

    # First Question
    task0_1 = asyncio.create_task(ask_dish_or_ingredient_coro(my_dish, async_client, start_time))
    # TODO 追加ホワイトリスト　ラーメン　ドーナツ　からあげ　えびせんべい（粉末とか桜えびの小さいやつなら大丈夫）
    task0_2 = asyncio.create_task(check_white_list_dish_coro(my_dish, "ラーメン", "raamen", "麺に卵が入っていても少量なので大丈夫です！", async_client, 1, start_time))
    task0_3 = asyncio.create_task(check_white_list_dish_coro(my_dish, "ドーナツ", "doughnut", "卵が入っていても量的に1つまでなら大丈夫です！", async_client, 1, start_time))
    task0_4 = asyncio.create_task(check_white_list_dish_coro(my_dish, "からあげ", "fried_chicken", "衣に卵が入っていても少量なので大丈夫です！", async_client, 1, start_time))
    task0 = [task0_1, task0_2, task0_3, task0_4]
    for completed_task in asyncio.as_completed(task0):
        key, result, reason = await completed_task
        my_dict[key] = result
        if reason:
            my_dict["reason"] = reason
        yield f"data: {json.dumps({'type': key, 'result': result, 'reason': reason}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない

    # Second Question
    if my_dict["dish_tf"]:
        task1_1 = asyncio.create_task(ask_dish_details_coro(my_dish, async_client, start_time))
        
        task1 = [task1_1]
        for completed_task in asyncio.as_completed(task1):
            key, result = await completed_task
            my_dict[key] = result
            yield f"data: {json.dumps({'type': key, 'result': result}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない

        print(my_dict)

    # Third Question
    tasks2 = []
    print(f"Current working directory: {os.getcwd()}")
    with open("backend/allergen.yaml", "r", encoding="utf-8") as f:
        allergen_dict = yaml.safe_load(f)
    i = 0
    for allergen_name, allergen_eng in allergen_dict.items():
        i += 1
        # ジャガイモとさつまいもを同時に含む場合対応できない。さつまいもはホワイトリスト的に使っているから注意。
        tasks2.append(asyncio.create_task(check_ingredient_coro(my_dish, allergen_name, allergen_eng, my_dict, async_client, i, start_time)))

    for completed_task in asyncio.as_completed(tasks2):
        key, result = await completed_task
        my_dict[key] = result
        yield f"data: {json.dumps({'type': key, 'result': result}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない
    result = (my_dict["raamen_tf"] or my_dict["doughnut_tf"] or my_dict["fried_chicken_tf"]) or (my_dict["egg_tf"] and potato_logic(my_dict["potato_tf"], my_dict["sweetpotato_tf"]) and my_dict["raw_vegetables_tf"] and my_dict["nuts_tf"] and my_dict["burdock_tf"] and my_dict["lotus_tf"] and my_dict["konjac_tf"] and my_dict["buckwheat_tf"])
    if result:
        if not my_dict["reason"]:
            if not my_dict["sweetpotato_tf"]:
                my_dict["reason"] = "芋は食べられないけど、さつまいもは大丈夫です！"
            else:
                my_dict["reason"] = "食べられます！"
    else:
        my_dict["reason"] = "食べられません！"
    yield f"data: {json.dumps({'type': 'safe_to_eat', 'result': result, 'reason': my_dict["reason"]}, ensure_ascii=False)}\n\n"  # 日本語をエスケープしない
    
    add_to_database(my_dict)

def potato_logic(potato, sweetpotato):
    return (not potato and not sweetpotato) or (potato and True)

def add_to_database(data_dict):
    """
    data_dict をデータベースに追加します。

    Parameters:
        data_dict (dict): type をキー、result を値とする辞書
    """
    try:
        with sqlite3.connect("data/allergies.db") as conn:
            cursor = conn.cursor()

            # テーブルを作成（必要に応じて）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS allergies (
                    type TEXT,
                    result TEXT
                )
            ''')

            # 辞書の内容をデータベースに挿入
            for type_key, result_value in data_dict.items():
                cursor.execute('''
                    INSERT INTO allergies (type, result)
                    VALUES (?, ?)
                ''', (type_key, str(result_value)))  # result を文字列として格納
            
            # コミットして保存
            conn.commit()

        return {"message": "データが正常に登録されました"}

    except sqlite3.Error as e:
        return {"message": f"データベースエラー: {e}"}

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
            async for chunk in create_tasks_coro(dish_name):
                yield chunk.encode("utf-8")  # UTF-8 にエンコード

        return Response(stream(), mimetype='text/event-stream')

    @my_app.route('/info', methods=['GET'])
    async def get_all_allergies():
        try:
            with sqlite3.connect("data/allergies.db") as conn:
                cursor = conn.cursor()
                
                # クエリを実行してデータを取得
                cursor.execute("SELECT type, result FROM allergies")
                rows = cursor.fetchall()

                # データを辞書形式に変換
                data = [{"type": row[0], "result": row[1]} for row in rows]

            # JSON形式でデータを返す
            return await render_template('info.html', data=data)

        except sqlite3.Error as e:
            # エラーハンドリング
            return jsonify({
                "message": f"データベースエラー: {e}"
            }), 500



    return my_app

app = create_app()

