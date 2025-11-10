from src.openai import send_messages
import pytest
from unittest.mock import patch, MagicMock
from openai import APIError

def test_send_messages_success(monkeypatch):
  monkeypatch.setenv('OPENAI_API_KEY', 'testkey')
  monkeypatch.setenv('OPENAI_MODEL_NAME', 'testmodel')
  with patch('src.openai.OpenAI') as mock_client:
    mock_client.return_value.chat.completions.create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="テスト回答"))])
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
      'answer': 'テスト回答',
      'status': 'success'
    }
    mock_client.assert_called_once_with(api_key='testkey')
    mock_client.return_value.chat.completions.create.assert_called_once_with(model='testmodel', messages=messages)

def test_send_messages_api_error(monkeypatch):
  monkeypatch.setenv('OPENAI_API_KEY', 'testkey')
  monkeypatch.setenv('OPENAI_MODEL_NAME', 'testmodel')
  with patch('src.openai.OpenAI') as mock_client:
    mock_client.return_value.chat.completions.create.side_effect = APIError(message=None, request=None, body={'code': 'api_error'})
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
      'answer': '',
      'status': 'API_ERROR'
    }
    mock_client.assert_called_once_with(api_key='testkey')
    mock_client.return_value.chat.completions.create.assert_called_once_with(model='testmodel', messages=messages)

def test_send_messages_messages_empty():
  messages = []
  with pytest.raises(ValueError, match='送信するメッセージが空です'):
    send_messages(messages)
