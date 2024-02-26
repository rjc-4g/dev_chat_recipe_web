import os
import sys
import pytest
from unittest.mock import MagicMock
from chatgptapi.services.chatgpt import createPrompt

# 環境変数とDjangoの設定
os.environ['DJANGO_SETTINGS_MODULE'] = 'devchatrecipe.settings'
sys.path.append('/backend/chatgptapi')

# Djangoのセットアップ
import django
django.setup()

MAX_LEN = 50

# テスト関数
def test_createPrompt_normal():
    # モックの設定
    request_data = {
        "prompt": {
            "appOverview": "test app",
            "programmingLanguage": 1,
            "platform": 2,
            "useDatabase": "true",
            "useCloud": "true"
        }
    }
    request = MagicMock()
    request.data = request_data

    # テスト対象の実行
    result = createPrompt(request)

    # 結果の検証
    assert result is not None

def test_createPrompt_abnormal():
    # モックの設定
    request_data = {
        "prompt": {
            "appOverview": "",
            "programmingLanguage": 1,
            "platform": 2,
            "useDatabase": "true",
            "useCloud": "true"
        }
    }
    request = MagicMock()
    request.data = request_data

    # テスト対象の実行
    result = createPrompt(request)

    # 結果の検証
    assert result == ""

def test_createPrompt_invalid_language_id():
    # モックの設定
    request_data = {
        "prompt": {
            "appOverview": "test app",
            "programmingLanguage": 999,
            "platform": 2,
            "useDatabase": "true",
            "useCloud": "true"
        }
    }
    request = MagicMock()
    request.data = request_data

    # テスト対象の実行
    result = createPrompt(request)

    # 結果の検証
    assert result == "存在しない言語です。入力内容を確認してください。"

def test_createPrompt_invalid_platform_id():
    # モックの設定
    request_data = {
        "prompt": {
            "appOverview": "test app",
            "programmingLanguage": 1,
            "platform": 999,  # 存在しないID
            "useDatabase": "true",
            "useCloud": "true"
        }
    }
    request = MagicMock()
    request.data = request_data

    # テスト対象の実行
    result = createPrompt(request)

    # 結果の検証
    assert result == "存在しないプラットフォームです。入力内容を確認してください。"

def test_createPrompt_app_overview_exceeds_max_len():
    # モックの設定
    long_string = "a" * (MAX_LEN + 1)
    request_data = {
        "prompt": {
            "appOverview": long_string,
            "programmingLanguage": 1,
            "platform": 2,
            "useDatabase": "true",
            "useCloud": "true"
        }
    }
    request = MagicMock()
    request.data = request_data

    # テスト対象の実行
    result = createPrompt(request)

    # 結果の検証
    assert result == "max_len_error"