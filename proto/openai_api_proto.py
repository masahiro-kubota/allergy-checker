#!/usr/bin/env python

import os

from dotenv import load_dotenv
from openai import OpenAI


if __name__=="__main__":
    load_dotenv()
    application_id = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    stream = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": "Please tell me about Shinzo Abe."}],
      stream=True
    )

    for chunk in stream:
      if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")

    print("\n")
    print("Finished Streaming!")

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": "Please tell me about Shinzo Abe."}],
      stream=False
    )

    print(response.choices[0].message)

    print("Finished Responsing!")
