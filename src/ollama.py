import os
from dotenv import load_dotenv
from ollama import chat, RequestError, ResponseError

load_dotenv(override=True)

def send_messages(messages):
  if not messages:
    raise ValueError('送信するメッセージが空です')
  try:
    response = chat(
      model=os.getenv('OLLAMA_MODEL_NAME'),
      options={},
      messages=messages
    )
  except RequestError as e:
    result = {
      'answer': '',
      'status': 'REQUEST_ERROR'
    }
  except ResponseError as e:
    result = {
      'answer': '',
      'status': 'RESPONSE_ERROR'
    }
  except ConnectionError as e:
    result = {
      'answer': '',
      'status': 'CONNECTION_ERROR'
    }
  else:
    result = {
      'answer': response['message']['content'],
      'status': 'success'
    }

  return result
