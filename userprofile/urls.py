from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('lessons/', views.lessons, name='lessons'),
]
