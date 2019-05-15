from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('recog/<slug:face_encoding>/', views.return_recognition_result, name='recog'),
]