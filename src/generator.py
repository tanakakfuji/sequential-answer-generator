from src.openai import send_messages as request_openai
from src.ollama import send_messages as request_ollama
import os
from dotenv import load_dotenv
import time
from tqdm import tqdm

load_dotenv(override=True)

def generate(client, system_prompt, queries_list, row_count):
  outputs = []
  total_error = 0
  continuous_error = 0
  with tqdm(total = row_count) as progress:
    for queries in queries_list:
      results = _execute_requests(client, system_prompt, queries)
      # 連続したAPIエラーへの対処
      if results[-1]['status'] == 'success':
        continuous_error = 0
      else:
        total_error += 1
        continuous_error += 1
      if continuous_error == 5:
        raise RuntimeError('API呼び出しが5回連続して失敗したため、処理を停止します')
      for i in range(len(queries)):
        outputs.append(queries[i]|results[i])
      progress.update(len(queries))
  return outputs, total_error
    
def _execute_requests(client, system_prompt, queries):
  results = []
  messages = [{'role': 'system','content': system_prompt}]
  for i, q in enumerate(queries):
    messages.append({'role': 'user','content': q['query']})
    if client == 'openai':
      result = request_openai(messages)
    elif client == 'ollama':
      result = request_ollama(messages)
    else:
      raise ValueError('clientオプションの値が不正です')
    time.sleep(float(os.getenv('REQUEST_INTERVAL_TIME')))

    if result['status'] == 'success':
      results.append(result)
      messages.append({'role': 'assistant','content': result['answer']})
    else:
      # エラーの場合、以降の回答は空にする
      for _ in range(len(queries) - i):
        results.append(result)
      break
    # 古い対話履歴はメッセージから削除する
    if i >= int(os.getenv('CONVERSATION_BUFFER_TURNS')) - 1:
      messages.pop(2)
      messages.pop(1)

  return results
