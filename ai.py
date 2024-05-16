import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # This loads the environment variables from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("API key missing")

#model = "gpt-3.5-turbo"
#model = 'gpt-4-turbo-preview'
model = "gpt-4o"

client = OpenAI(api_key=api_key)


def ask(prompt, conversation=None, expect_json=False):
    m = {"role": "user", "content": prompt}
    if conversation is None:
        messages = [m]
    else:
        conversation.append(m)
        messages = conversation
    rf = {"type": "json_object"} if expect_json else None
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        response_format=rf,
        temperature=1.0
    )
    response = chat_completion.choices[0].message
    if conversation != None:
        conversation.append(response)
    return response.content


""" conversation = []
p = input("What's your prompt? ")
while p != "stop":
    response = ask(p, conversation)
    print(response)
    p = input()
 """