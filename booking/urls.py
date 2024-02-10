from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('booking_2', views.booking_2, name='booking_2'),
    # path('<str:tab>/', views.booking, name='booking_with_tab'),
]
