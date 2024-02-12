from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    readonly_fields = (
        'booking_reference',
        'booked_on',
        'price',
        'stripe_pid',
    )

    fields = (
              'full_name', 'email',
              'lesson_type', 'lesson_date', 'lesson_time',
              'house_no', 'street',
              'town', 'post_code',
              'billpayer_name',
              'billpayer_house_no',
              'billpayer_street',
              'billpayer_town',
              'billpayer_post_code',
            )

    list_display = ('booking_reference', 'booked_on',
                    'full_name',
                    'email',
                    'lesson_type', 'lesson_date', 'lesson_time',
                    'house_no', 
                    'street',
                    'town',
                    'post_code',
                    'price',
                    'billpayer_name',
                    'billpayer_house_no',
                    'billpayer_street',
                    'billpayer_town',
                    'billpayer_post_code',
                )

    ordering = ('-booked_on',)

admin.site.register(Booking, BookingAdmin)