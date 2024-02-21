import uuid

from django.db import models

from django.conf import settings

from datetime import datetime
from decimal import Decimal

from userprofile.models import UserProfile
from checkout.models import Price

LESSON_TYPE_MANUAL = "Manual"
LESSON_TYPE_AUTOMATIC = "Automatic"
LESSON_TYPE_MOCK_TEST = "Mock Test"

LESSON_TYPE_CHOICES = [
    (LESSON_TYPE_MANUAL, "Manual"),
    (LESSON_TYPE_AUTOMATIC, "Automatic"),
    (LESSON_TYPE_MOCK_TEST, "Mock Test"),
]


class Booking(models.Model):
    booking_reference = models.CharField(max_length=32, null=False, editable=False)

    cancelled = models.BooleanField(null=True, blank=True, default=False)
    refunded = models.BooleanField(null=True, blank=True, default=False)
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    
    lesson_type = models.CharField(choices=LESSON_TYPE_CHOICES, max_length=20, null=False, blank=False, default='')

    lesson_date = models.DateField(null=True, blank=True)
    lesson_time = models.TimeField(null=True, blank=True)
    
    house_no = models.CharField(max_length=40, null=False, blank=False, default='')
    street = models.CharField(max_length=100, null=False, blank=False, default='')
    town = models.CharField(max_length=40, null=False, blank=False, default='')
    post_code = models.CharField(max_length=7, null=False, blank=False, default='')
    
    booked_on = models.DateTimeField(auto_now_add=True)

    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    
    billpayer_name = models.CharField(max_length=50, null=False, blank=False, default='')
    billpayer_house_no = models.CharField(max_length=40, null=False, blank=False, default='')
    billpayer_street = models.CharField(max_length=100, null=False, blank=False, default='')
    billpayer_town = models.CharField(max_length=40, null=False, blank=False, default='')
    billpayer_post_code = models.CharField(max_length=10, null=False, blank=False, default='')


    def _generate_booking_reference(self):
        """
        Generate a random, unique booking reference number using UUID
        """
        return uuid.uuid4().hex.upper()

    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self._generate_booking_reference()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_reference

    class Meta:
        verbose_name = 'Lesson Booking'
        verbose_name_plural = 'Lesson Bookings'