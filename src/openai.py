import os
from dotenv import load_dotenv
from openai import OpenAI, APIError

load_dotenv(override=True)

def send_messages(messages):
  if not messages:
    raise ValueError('送信するメッセージが空です')
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  try:
    response = client.chat.completions.create(
        model=os.getenv('OPENAI_MODEL_NAME'),
        messages=messages
    )
  except APIError as e:
    result = {
      'text': '',
      'status': e.code.upper()
    }
  else:
    result = {
      'text': response.choices[0].message.content,
      'status': 'success'
    }

  return result
