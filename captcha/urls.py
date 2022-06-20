from django.urls import path
from . import views


urlpatterns = [
    path('', views.captcha_session, name='captcha_session'),
]