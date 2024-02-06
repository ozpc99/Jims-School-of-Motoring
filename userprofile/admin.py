from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fields = ('full_name', 'email',
              'phone')
admin.site.register(UserProfile, UserProfileAdmin)