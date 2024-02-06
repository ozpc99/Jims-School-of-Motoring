from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import models

from django.conf import settings

from datetime import datetime, timedelta

from .models import UserProfile
from booking.models import Booking

from .forms import *

now = datetime.now()

# Profile Page View
def profile(request):
    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    """ Gets all bookings made by and associated with the user """
    all_bookings = profile.bookings.all().order_by('lesson_date', 'lesson_time')

    """
    Gets all bookings with a 'lesson_date' that is
    greater than or equal to the date now and greater than the time now.
    (today or in the future)
    """
    upcoming_bookings = profile.bookings.filter(
        models.Q(lesson_date__gt=now.date()) | 
        (models.Q(lesson_date=now.date(), lesson_time__gt=now.time()))
    ).order_by('lesson_date', 'lesson_time')

    """
    Queries the UserProfile booking object for
    a booking with a lesson_type that matches 'Mock Test'.
    Singles out that specific booking object
    and returns it's associated values. 
    """
    def find_mock_test_booking(all_bookings):
        for booking in all_bookings:
            if booking.lesson_type == "Mock Test":
                return booking.lesson_date, booking.lesson_time, booking.house_no, booking.post_code
    mock_test_booking = find_mock_test_booking(all_bookings)

    profile_first_name = profile.first_name

    """ A view to render the User Profile page. """
    template = 'userprofile/profile.html'
    context = {
        'profile': profile,
        'profile_first_name': profile_first_name,
        'now': now,
        'all_bookings': all_bookings,
        'upcoming_bookings': upcoming_bookings,
        'mock_test_booking': mock_test_booking,
        'on_profile_page': True,
    }

    return render(request, template, context)
