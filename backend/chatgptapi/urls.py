from django.urls import path

from . import views

urlpatterns = [
    path("chatgpt/prompt", views.RequestChatGPTView.as_view()),
    path("chatgpt/selection/languages", views.RequestChatGPTSelectionLang.as_view()),
    path("chatgpt/selection/platforms", views.RequestChatGPTSelectionPlatform.as_view())
]
