# 簡易版辞書データ（料理名: 材料リスト）
recipe_database = {
    "オムライス": ["卵", "鶏肉", "ご飯", "ケチャップ"],
    "豆乳スープ": ["豆乳", "白菜", "豚肉", "塩"],
    "フライドチキン": ["鶏肉", "小麦粉", "油", "卵", "豆"],
}

# アレルゲンのリスト
allergens = ["卵", "豆"]

# アレルゲン判定関数
def check_allergens_in_recipe(recipe_name):
    ingredients = recipe_database.get(recipe_name)
    if not ingredients:
        return f"料理名 '{recipe_name}' のレシピが見つかりません。"
    # 原材料の中にアレルゲンが含まれているかチェック
    detected_allergens = []
    for i in ingredients:
        for a in allergens:
            if a in i:
                detected_allergens.append(a)

    return f"この料理にはアレルゲンが含まれています: {','.join(detected_allergens)}"

print(check_allergens_in_recipe("オムライス"))  # Output: この料理には以下のアレルゲンが含まれています: 卵
print(check_allergens_in_recipe("豆乳スープ"))  # Output: この料理には以下のアレルゲンが含まれています: 豆
print(check_allergens_in_recipe("フライドチキン"))  # Output: この料理には以下のアレルゲンが含まれています: 卵
print(check_allergens_in_recipe("カレー"))  # Output: 料理名 'カレー' のレシピが見つかりません。