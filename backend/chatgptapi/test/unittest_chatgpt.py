import os
from django.conf import settings
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'devchatrecipe.settings'
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from chatgptapi.services.chatgpt import createPrompt

import sys
sys.path.append('/backend/chatgptapi')

class TestChatGPT(unittest.TestCase):
    MAX_LEN = 50

    def test_createPrompt_normal(self):
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
        self.assertIsNotNone(result)

    def test_createPrompt_abnormal(self):
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
        self.assertEqual(result, "")

    def test_createPrompt_invalid_language_id(self):
        # モックの設定
        request_data = {
            "prompt": {
                "appOverview": "test app",
                "programmingLanguage": 999,  # 存在しないID
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
        self.assertEqual(result, "存在しない言語です。入力内容を確認してください。")

    def test_createPrompt_invalid_platform_id(self):
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
        self.assertEqual(result, "存在しないプラットフォームです。入力内容を確認してください。")

    def test_createPrompt_app_overview_exceeds_max_len(self):
        # モックの設定
        long_string = "a" * (self.MAX_LEN + 1)
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
        self.assertEqual(result, "max_len_error")

if __name__ == '__main__':
    unittest.main()