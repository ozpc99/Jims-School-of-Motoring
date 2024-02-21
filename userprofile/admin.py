from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'phone',
        'home_house_no',
        'home_post_code',
    )
    fields = (
        'user',
        'first_name',
        'last_name',
        'phone',
        'license_no',
        'license_expiry',
        'home_house_no',
        'home_street',
        'home_town',
        'home_post_code',
        'theory_test_date',
        'theory_test_center',
        'mock_test_date',
        'mock_test_address',
        'practical_test_date',
        'practical_test_center',
    )
admin.site.register(UserProfile, UserProfileAdmin)