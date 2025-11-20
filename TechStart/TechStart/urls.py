from django.contrib import admin
from django.urls import path
from .views import home_view, learning_options_view, topic_selection_view, chat_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('start/', learning_options_view, name='learning_options'),
    path('learn/<str:path>/', topic_selection_view, name='topic_selection'),
    path('chat/', chat_view, name='chat'),
]

