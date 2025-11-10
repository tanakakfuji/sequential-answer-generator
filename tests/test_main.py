from src.main import _build_data
import pytest

def test_build_data_success():
  data = [
    ['conversation_id', 'query'],
    ['1111', 'テスト質問1'],
    ['2222', 'テスト質問1'],
    ['2222', 'テスト質問2'],
    ['2222', 'テスト質問3'],
    ['1111', 'テスト質問2']
  ]
  assert _build_data(data) == [
    [{'conversation_id': '1111', 'query': 'テスト質問1'}, {'conversation_id': '1111', 'query': 'テスト質問2'}],
    [{'conversation_id': '2222', 'query': 'テスト質問1'}, {'conversation_id': '2222', 'query': 'テスト質問2'}, {'conversation_id': '2222', 'query': 'テスト質問3'}]
  ]

def test_build_data_conersation_id_missing():
  data = [
    ['discussion_id', 'query'],
    ['1111', 'テスト質問1'],
    ['2222', 'テスト質問1'],
    ['2222', 'テスト質問2'],
    ['2222', 'テスト質問3'],
    ['1111', 'テスト質問2']
  ]
  with pytest.raises(KeyError, match='csvファイルにはconversation_id、queryキーが必要です'):
    _build_data(data)

def test_build_data_query_missing():
  data = [
    ['conversation_id', 'question'],
    ['1111', 'テスト質問1'],
    ['2222', 'テスト質問1'],
    ['2222', 'テスト質問2'],
    ['2222', 'テスト質問3'],
    ['1111', 'テスト質問2']
  ]
  with pytest.raises(KeyError, match='csvファイルにはconversation_id、queryキーが必要です'):
    _build_data(data)

def test_build_data_conversation_id_empty():
  data = [
    ['conversation_id', 'query'],
    ['1111', 'テスト質問1'],
    ['', 'テスト質問1'],
    ['2222', 'テスト質問2'],
    ['2222', 'テスト質問3'],
    ['1111', 'テスト質問2']
  ]
  with pytest.raises(ValueError, match='2行目のconversaion_idが空です'):
    _build_data(data)

def test_build_data_query_empty():
  data = [
    ['conversation_id', 'query'],
    ['1111', 'テスト質問1'],
    ['2222', ''],
    ['2222', 'テスト質問2'],
    ['2222', 'テスト質問3'],
    ['1111', 'テスト質問2']
  ]
  with pytest.raises(ValueError, match='2行目のqueryが空です'):
    _build_data(data)
