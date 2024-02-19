from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    # Profile | Update Profile Details
    path('update_name/', views.update_name, name='update_name'),
    path('update_phone/', views.update_phone, name='update_phone'),
    path('update_address/', views.update_address, name='update_address'),
    path('update_license/', views.update_license, name='update_license'),
    path('update_theory_test/', views.update_theory_test, name='update_theory_test'),
    path('update_practical_test/', views.update_practical_test, name='update_practical_test'),
    path('lessons/', views.lessons, name='lessons'),
    path('invoice/<booking_reference>/', views.invoice, name='invoice'),
    path('cancel/<booking_reference>/', views.cancel, name='cancel'),
]
