from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from .services.chatgpt import createPrompt

import json


class RequestChatGPTView(APIView):
    def post(self, request, format=None):
        try:
            # 質問結果取得
            content = createPrompt(request)

            if not content:
                return Response(
                    {"content": "結果が取得できませんでした。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif content == "max_len_error":
                return Response(
                    {"content": "入力項目の桁数が上限を超えています。"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                return Response(
                    {"content": content}, status=status.HTTP_200_OK
                )
        except Exception as e:
            # エラーが発生した場合
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestChatGPTSelectionLang(APIView):
    def get(self, request, format=None):
        try:
            # 言語
            programming_language_open = open('./json/programmingLanguage.json', 'r')
            programming_language_json = json.load(programming_language_open)["lang"]
            return Response(
                str(programming_language_json), status=status.HTTP_200_OK
            )
        except Exception as e:
            # エラーが発生した場合
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestChatGPTSelectionPlatform(APIView):
    def get(self, request, format=None):
        try:
            # プラットフォーム
            platform_open = open('./json/platform.json', 'r')
            platform_json = json.load(platform_open)["platform"]
            return Response(
                str(platform_json), status=status.HTTP_200_OK
            )
        except Exception as e:
            # エラーが発生した場合
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
