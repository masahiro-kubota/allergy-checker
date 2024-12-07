import json
import sys

import requests
import yaml

# API URL
API_URL = "https://allergy-checker.onrender.com/check_allergy_stream"

# 期待される結果

with open("test/expected_results.yaml", "r", encoding="utf-8") as f:
    EXPECTED_RESULTS = yaml.safe_load(f)

def test_safe_to_eat(dish_name, expected_result):
    try:
        # APIにリクエストを送信
        response = requests.get(f"{API_URL}?dish_name={dish_name}", stream=True, timeout=60)

        if response.status_code != 200:
            raise Exception(f"Received status code {response.status_code}")

        # レスポンスデータを確認
        for line in response.iter_lines():
            if line:
                # デコードしたラインから 'data: ' プレフィックスを除去
                line_text = line.decode('utf-8')
                if not line_text.startswith('data: '):
                    continue

                # 'data: ' を除去してJSONをパース
                json_str = line_text[6:]  # 'data: ' の長さが6なので、それ以降の部分を取得
                print(json_str)
                data = json.loads(json_str)

                # "safe_to_eat" の結果をチェック
                if data["type"] == "safe_to_eat":
                    assert data["result"] == expected_result, f"Expected {expected_result}, but got {data['result']}"
                    print(f"{dish_name}: safe_to_eat test passed")
                    return
        # "safe_to_eat" が見つからなかった場合
        raise Exception(f"'safe_to_eat' key not found in the response")
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    errors = {}  # 失敗した料理とエラー内容を記録

    for dish_name, expected_result in EXPECTED_RESULTS.items():
        print(f"Testing: {dish_name}")
        error = test_safe_to_eat(dish_name, expected_result)
        if error:
            errors[dish_name] = error

    # テスト結果を出力
    if errors:
        print("\nSome tests failed:")
        for dish, error in errors.items():
            print(f"- {dish}: {error}")
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)