#!/usr/bin/env python

import os

from dotenv import load_dotenv
from openai import OpenAI

#def generate_ingredients(dish_name);:

if __name__=="__main__":
    load_dotenv()
    application_id = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    dish_name = input('料理名を入力してください: ')
    stream = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content":
            f"""
次の料理の主要な原材料を5つ考えて、そこに卵が入るかどうかをTrue/Falseで答えてください。回答はTrue/Falseのどちらかのみを答えてください。

料理名: {dish_name}
原材料:
    """}],
      stream=True
    )

    for chunk in stream:
      if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

    print("\n")
    print("Finished Streaming!")
"""
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": "Please tell me about Shinzo Abe."}],
      stream=False
    )

    print(response.choices[0].message)

    print("Finished Responsing!")
"""