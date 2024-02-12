from django.contrib import admin
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<booking_reference>/', views.success, name='success'),
    path('wh/', webhook, name='webhook'),
]
