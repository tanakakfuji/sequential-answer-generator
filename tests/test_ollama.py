from src.ollama import send_messages
import pytest
from unittest.mock import patch
from ollama import RequestError, ResponseError

def test_send_messages_success(monkeypatch):
  monkeypatch.setenv('OLLAMA_MODEL_NAME', 'testmodel')
  with patch('src.ollama.chat', return_value={'message': {'content': 'テスト回答'}}) as mock_chat:
    messages = [
      {
        'role': 'system',
        'content': 'テストシステムプロンプト'
      },
      {
        'role': 'user',
        'content': 'テスト質問'
      }
    ]
    assert send_messages(messages) == {
      'text': 'テスト回答',
      'status': 'success'
    }
    mock_chat.assert_called_once_with(model='testmodel', options={}, messages=messages)

def test_send_messages_request_error(monkeypatch):
  monkeypatch.setenv('OLLAMA_MODEL_NAME', 'testmodel')
  with patch('src.ollama.chat') as mock_chat:
    mock_chat.side_effect = RequestError('テストエラー')
    messages = [
      {
        'role': 'system',
        'content': 'テストシステムプロンプト'
      },
      {
        'role': 'user',
        'content': 'テスト質問'
      }
    ]
    assert send_messages(messages) == {
      'text': '',
      'status': 'REQUEST_ERROR'
    }
    mock_chat.assert_called_once_with(model='testmodel', options={}, messages=messages)

def test_send_messages_response_error(monkeypatch):
  monkeypatch.setenv('OLLAMA_MODEL_NAME', 'testmodel')
  with patch('src.ollama.chat') as mock_chat:
    mock_chat.side_effect = ResponseError('テストエラー')
    messages = [
      {
        'role': 'system',
        'content': 'テストシステムプロンプト'
      },
      {
        'role': 'user',
        'content': 'テスト質問'
      }
    ]
    assert send_messages(messages) == {
      'text': '',
      'status': 'RESPONSE_ERROR'
    }
    mock_chat.assert_called_once_with(model='testmodel', options={}, messages=messages)

def test_send_messages_connection_error(monkeypatch):
  monkeypatch.setenv('OLLAMA_MODEL_NAME', 'testmodel')
  with patch('src.ollama.chat') as mock_chat:
    mock_chat.side_effect = ConnectionError('テストエラー')
    messages = [
      {
        'role': 'system',
        'content': 'テストシステムプロンプト'
      },
      {
        'role': 'user',
        'content': 'テスト質問'
      }
    ]
    assert send_messages(messages) == {
      'text': '',
      'status': 'CONNECTION_ERROR'
    }
    mock_chat.assert_called_once_with(model='testmodel', options={}, messages=messages)

def test_send_messages_messages_empty():
  messages = []
  with pytest.raises(ValueError, match='送信するメッセージが空です'):
    send_messages(messages)
