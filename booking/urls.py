from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('booking_2', views.booking_2, name='booking_2'),
    path('booking_3', views.booking_3, name='booking_3'),
    path('booking_4', views.booking_4, name='booking_4'),
]
