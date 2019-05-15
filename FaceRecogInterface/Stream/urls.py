from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.return_stream, name='return_stream'),
    path('generate_stream/', views.generate_stream, name='generate_stream'),
    path('request_recognition/', views.request_recognition, name='request_recognition'),
]