from django.contrib import admin
from .models import Booking
from checkout.models import Price

class BookingAdmin(admin.ModelAdmin):
    readonly_fields = (
        'booking_reference',
        'booked_on',
        'stripe_pid',
    )

    fields = (
            'full_name', 'email', 'user_profile',
            'lesson_type', 'lesson_date', 'lesson_time',
            'house_no', 'street',
            'town', 'post_code',
            'cancelled',
            'refunded',
            'price',
            'billpayer_name',
            'billpayer_house_no',
            'billpayer_street',
            'billpayer_town',
            'billpayer_post_code',
        )

    list_display = ('booking_reference', 'booked_on',
                    'cancelled', 'refunded',
                    'full_name',
                    'user_profile',
                    'email',
                    'lesson_type', 'lesson_date', 'lesson_time',
                    'house_no', 
                    'street',
                    'town',
                    'post_code',
                    'price',
                )

    ordering = ('-booked_on',)

admin.site.register(Booking, BookingAdmin)