import os
import time
from dotenv import load_dotenv
from collections import defaultdict
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
      'text': '',
      'status': 'REQUEST_ERROR'
    }
  except ResponseError as e:
    result = {
      'text': '',
      'status': 'RESPONSE_ERROR'
    }
  except ConnectionError as e:
    result = {
      'text': '',
      'status': 'CONNECTION_ERROR'
    }
  else:
    result = {
      'text': response['message']['content'],
      'status': 'success'
    }

  return result
