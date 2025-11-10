from src.generator import generate, _execute_requests
import pytest
from unittest.mock import Mock, patch, call, DEFAULT
from copy import deepcopy

SYSTEM_PROMPT = 'テストシステムプロンプト'
QUERIES = [{'conversation_id': '1', 'query': '質問1'},{'conversation_id': '1', 'query': '質問2'},{'conversation_id': '1', 'query': '質問3'},{'conversation_id': '1', 'query': '質問4'}]
QUERIES_LIST = [
  [{'conversation_id': '1', 'query': 'テスト質問'}, {'conversation_id': '1', 'query': 'テスト質問'}],
  [{'conversation_id': '2', 'query': 'テスト質問'}, {'conversation_id': '2', 'query': 'テスト質問'}],
  [{'conversation_id': '3', 'query': 'テスト質問'}, {'conversation_id': '3', 'query': 'テスト質問'}],
  [{'conversation_id': '4', 'query': 'テスト質問'}, {'conversation_id': '4', 'query': 'テスト質問'}],
  [{'conversation_id': '5', 'query': 'テスト質問'}, {'conversation_id': '5', 'query': 'テスト質問'}],
  [{'conversation_id': '6', 'query': 'テスト質問'}, {'conversation_id': '6', 'query': 'テスト質問'}],
]

def test_generate_without_errors():
  with(patch('src.generator._execute_requests', return_value=[{'answer': 'テスト回答', 'status': 'success'} for _ in range(len(QUERIES_LIST[0]))]) as mock_execute):
    client = 'openai'
    row_count = sum(len(inner_list) for inner_list in QUERIES_LIST)
    assert generate(client, SYSTEM_PROMPT, QUERIES_LIST, row_count) == (
      [
        {'conversation_id': '1', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '1', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '2', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '2', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '3', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '3', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '4', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '4', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '5', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '5', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '6', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '6', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
      ],
      0
    )
    mock_execute.assert_has_calls(calls=[
      call(client, SYSTEM_PROMPT, [{'conversation_id': '1', 'query': 'テスト質問'}, {'conversation_id': '1', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '2', 'query': 'テスト質問'}, {'conversation_id': '2', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '3', 'query': 'テスト質問'}, {'conversation_id': '3', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '4', 'query': 'テスト質問'}, {'conversation_id': '4', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '5', 'query': 'テスト質問'}, {'conversation_id': '5', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '6', 'query': 'テスト質問'}, {'conversation_id': '6', 'query': 'テスト質問'}]),
    ])

def test_generate_with_api_error():
  with(patch('src.generator._execute_requests') as mock_execute):
    mock_execute.side_effect = [
      [{'answer': 'テスト回答', 'status': 'success'} for _ in range(len(QUERIES_LIST[0]))],
      [{'answer': '', 'status': 'API_ERROR'} for _ in range(len(QUERIES_LIST[0]))],
      [{'answer': 'テスト回答', 'status': 'success'} for _ in range(len(QUERIES_LIST[0]))],
      [{'answer': '', 'status': 'API_ERROR'} for _ in range(len(QUERIES_LIST[0]))],
      [{'answer': 'テスト回答', 'status': 'success'} for _ in range(len(QUERIES_LIST[0]))],
      [{'answer': '', 'status': 'API_ERROR'} for _ in range(len(QUERIES_LIST[0]))]
    ]
    client = 'openai'
    row_count = sum(len(inner_list) for inner_list in QUERIES_LIST)
    assert generate(client, SYSTEM_PROMPT, QUERIES_LIST, row_count) == (
      [
        {'conversation_id': '1', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '1', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '2', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'}, {'conversation_id': '2', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'},
        {'conversation_id': '3', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '3', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '4', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'}, {'conversation_id': '4', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'},
        {'conversation_id': '5', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'}, {'conversation_id': '5', 'query': 'テスト質問', 'answer': 'テスト回答', 'status': 'success'},
        {'conversation_id': '6', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'}, {'conversation_id': '6', 'query': 'テスト質問', 'answer': '', 'status': 'API_ERROR'},
      ],
      3
    )
    mock_execute.assert_has_calls(calls=[
      call(client, SYSTEM_PROMPT, [{'conversation_id': '1', 'query': 'テスト質問'}, {'conversation_id': '1', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '2', 'query': 'テスト質問'}, {'conversation_id': '2', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '3', 'query': 'テスト質問'}, {'conversation_id': '3', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '4', 'query': 'テスト質問'}, {'conversation_id': '4', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '5', 'query': 'テスト質問'}, {'conversation_id': '5', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '6', 'query': 'テスト質問'}, {'conversation_id': '6', 'query': 'テスト質問'}]),
    ])

def test_generate_continuous_api_errors():
  client = 'openai'
  row_count = sum(len(inner_list) for inner_list in QUERIES_LIST)
  with (
    patch('src.generator._execute_requests', return_value=[{'answer': '', 'status': 'API_ERROR'} for _ in range(len(QUERIES_LIST[0]))]) as mock_execute,
    pytest.raises(RuntimeError, match='API呼び出しが5回連続して失敗したため、処理を停止します')
  ):
    generate(client, SYSTEM_PROMPT, QUERIES_LIST, row_count)
    mock_execute.assert_has_calls(calls=[
      call(client, SYSTEM_PROMPT, [{'conversation_id': '1', 'query': 'テスト質問'}, {'conversation_id': '1', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '2', 'query': 'テスト質問'}, {'conversation_id': '2', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '3', 'query': 'テスト質問'}, {'conversation_id': '3', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '4', 'query': 'テスト質問'}, {'conversation_id': '4', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '5', 'query': 'テスト質問'}, {'conversation_id': '5', 'query': 'テスト質問'}]),
      call(client, SYSTEM_PROMPT, [{'conversation_id': '6', 'query': 'テスト質問'}, {'conversation_id': '6', 'query': 'テスト質問'}]),
    ])


def test_execute_requests_openai_success(monkeypatch):
  monkeypatch.setenv('CONVERSATION_BUFFER_TURNS', '2')
  monkeypatch.setenv('REQUEST_INTERVAL_TIME', '5.0')
  with (
    patch('src.generator.request_openai', return_value={'answer': 'テスト回答', 'status': 'success'}) as mock_request,
    patch('src.generator.time.sleep') as mock_sleep
  ):
    mock_request = copy_call_args(mock_request)
    client = 'openai'
    assert _execute_requests(client, SYSTEM_PROMPT, QUERIES) == [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'}
    ]
    mock_request.assert_has_calls(calls=[
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問1'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問1'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問2'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問2'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問3'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問3'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問4'},
      ])
    ])
    mock_sleep.assert_has_calls(calls=[
      call(5.0),
      call(5.0),
      call(5.0),
      call(5.0)
    ])

def test_execute_requests_ollama_success(monkeypatch):
  monkeypatch.setenv('CONVERSATION_BUFFER_TURNS', '2')
  monkeypatch.setenv('REQUEST_INTERVAL_TIME', '5.0')
  with (
    patch('src.generator.request_ollama', return_value={'answer': 'テスト回答', 'status': 'success'}) as mock_request,
    patch('src.generator.time.sleep') as mock_sleep
  ):
    mock_request = copy_call_args(mock_request)
    client = 'ollama'
    assert _execute_requests(client, SYSTEM_PROMPT, QUERIES) == [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'}
    ]
    mock_request.assert_has_calls(calls=[
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問1'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問1'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問2'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問2'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問3'},
      ]),
      call([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': '質問3'},
        {'role': 'assistant', 'content': 'テスト回答'},
        {'role': 'user', 'content': '質問4'},
      ])
    ])
    mock_sleep.assert_has_calls(calls=[
      call(5.0),
      call(5.0),
      call(5.0),
      call(5.0)
    ])

def test_execute_requests_openai_api_error(monkeypatch):
  monkeypatch.setenv('CONVERSATION_BUFFER_TURNS', '2')
  monkeypatch.setenv('REQUEST_INTERVAL_TIME', '5.0')
  with (
    patch('src.generator.request_openai') as mock_request,
    patch('src.generator.time.sleep') as mock_sleep
  ):
    mock_request.side_effect = [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': '', 'status': 'API_ERROR'}
    ]
    client = 'openai'
    assert _execute_requests(client, SYSTEM_PROMPT, QUERIES) == [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': '', 'status': 'API_ERROR'}
    ]
    assert mock_request.call_count == 4
    mock_sleep.assert_has_calls(calls=[
      call(5.0),
      call(5.0),
      call(5.0),
      call(5.0),
    ])

def test_execute_requests_ollama_api_error(monkeypatch):
  monkeypatch.setenv('CONVERSATION_BUFFER_TURNS', '2')
  monkeypatch.setenv('REQUEST_INTERVAL_TIME', '5.0')
  with (
    patch('src.generator.request_ollama') as mock_request,
    patch('src.generator.time.sleep') as mock_sleep
  ):
    mock_request.side_effect = [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': '', 'status': 'API_ERROR'},
    ]
    client = 'ollama'
    assert _execute_requests(client, SYSTEM_PROMPT, QUERIES) == [
      {'answer': 'テスト回答', 'status': 'success'},
      {'answer': '', 'status': 'API_ERROR'},
      {'answer': '', 'status': 'API_ERROR'},
      {'answer': '', 'status': 'API_ERROR'}
    ]
    assert mock_request.call_count == 2
    mock_sleep.assert_has_calls(calls=[
      call(5.0),
      call(5.0)
    ])

def test_execute_requests_client_invalid_value():
  client = 'sample'
  with pytest.raises(ValueError, match='clientオプションの値が不正です'):
    _execute_requests(client, SYSTEM_PROMPT, QUERIES)

# ミュータブルな引数をモックで適切に検証するために必要な関数（https://docs.python.org/ja/3/library/unittest.mock-examples.html#coping-with-mutable-arguments）
def copy_call_args(mock):
  new_mock = Mock()
  def side_effect(*args, **kwargs):
      args = deepcopy(args)
      kwargs = deepcopy(kwargs)
      new_mock(*args, **kwargs)
      return DEFAULT
  mock.side_effect = side_effect
  return new_mock
