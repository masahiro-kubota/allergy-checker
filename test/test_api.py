import requests
import json
import sys

# API URL
API_URL = "http://allergy-checker.onrender.com/check_allergy_stream"

# テストする料理名
DISH_NAME = "おでん"

def test_safe_to_eat():
    # APIにリクエストを送信
    response = requests.get("https://allergy-checker.onrender.com/check_allergy_stream?dish_name=%E3%81%8A%E3%81%A7%EF%BD%8E", stream=True, timeout=20)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        sys.exit(1)

    # レスポンスデータを確認
    for line in response.iter_lines():
        print(f"line: {line}")
        if line:
            # デコードしたラインから 'data: ' プレフィックスを除去
            line_text = line.decode('utf-8')
            if not line_text.startswith('data: '):
                continue
            
            # 'data: ' を除去してJSONをパース
            json_str = line_text[6:]  # 'data: ' の長さが6なので、それ以降の部分を取得
            print(f"json_str: {json_str}")
            try:
                data = json.loads(json_str)
                # safe_to_eatの結果をチェック
                if data["type"] == "safe_to_eat":
                    expected_result = False  # 想定される値
                    assert data["result"] == expected_result, f"Expected {expected_result}, but got {data['result']}"
                    print("safe_to_eat test passed")
                    return
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                continue

if __name__ == "__main__":
    test_safe_to_eat()
