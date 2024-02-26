from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from .services.chatgpt import createPrompt, get_programming_language, get_platform

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
            # 言語取得
            return Response(
                get_programming_language(), status=status.HTTP_200_OK
            )
        except Exception as e:
            # エラーが発生した場合
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestChatGPTSelectionPlatform(APIView):
    def get(self, request, format=None):
        try:
            # プラットフォーム取得
            return Response(
                get_platform(), status=status.HTTP_200_OK
            )
        except Exception as e:
            # エラーが発生した場合
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
