from django.urls import re_path
from . import views

app_name = 'chats'

urlpatterns = [
    re_path(r'^$', views.app, name='twilio'),
    re_path(r'^token', views.token, name='token'),
]
