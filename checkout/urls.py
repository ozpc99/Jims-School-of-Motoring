from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success', views.success, name='success'),
    # path('success/<booking_reference>', views.success, name='success'),
]
