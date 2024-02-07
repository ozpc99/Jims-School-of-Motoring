from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import models

from django.conf import settings

from datetime import datetime, timedelta

from django.contrib.auth.models import User

from .models import UserProfile
from booking.models import Booking

from .forms import *

now = datetime.now()

# Profile Page View
def profile(request):

    # Profile Info:

    """ Gets user object """
    user = request.user

    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    """
    Checks if user has completed profile or not.
    Displays welcome message.
    """
    if profile.first_name:
        welcome_message = f"Welcome back, {profile.first_name}"
    else:
        welcome_message = f"Welcome, {user.username}"

    """
    Checks if user has completed profile.
    Checks which parts of profile are incomplete.
    Displays toast/s to prompt user to finish filling in their profile.
    """
    if (
        hasattr(request.user, 'username') and request.user.username # Checks if user has a username
        and hasattr(request.user, 'email') and request.user.email # Checks if user has an email address
        and all(# Checks if user profile is not complete
                not getattr(profile, field.name) 
                for field in profile._meta.fields 
                if (
                    field.name != 'id'
                    and field.name != 'user'
                    and field.name != 'theory_test_date'
                    and field.name != 'theory_test_center'
                    and field.name != 'mock_test_date'
                    and field.name != 'practical_test_date'
                    and field.name != 'practical_test_center'
                )
            )
    ):
        messages.info(request, "Please finish setting up your profile.")



    """
    if not profile.first_name or not profile.last_name:
        messages.info(request, "You haven't told us your name")
    elif not profile.phone:
        messages.info(request, "Please provide your phone number. \
            We might need it if we need to get in touch on the day \
                of your lesson.")
    elif not profile.license_no:
        messages.info(request, "Please provide your \
            provisional license number. \
                Your instructor will need to verify your identity \
                    before you hit the road.")
    elif not profile.license_expiry:
        messages.info(request, "Please provide your \
            provisional license's expiry date. \
                We need to check it is valid.")
    elif (
        not profile.home_house_no
        or not profile.home_street
        or not profile.home_town
        or not profile.home_post_code
    ):
        messages.error(request, "Please finish filling out your \
            home address details.")
    elif not user.username:
        messages.error(request, "Hmm, that's odd. \
            It seems your username wasn't saved \
            to your profile when you registered. \
                Please contact us and we'll get this fixed.")
    elif not user.email:
        messages.error(request, "Hmm, that's odd. \
            It seems your email address wasn't saved \
            to your profile when you registered. \
                Please contact us and we'll get this fixed.")
    """

    # Booking Info:

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


    # Template and Context:
    """ A view to render the User Profile page. """
    template = 'userprofile/profile.html'
    context = {
        'profile': profile,
        'welcome_message': welcome_message,
        'now': now,
        'all_bookings': all_bookings,
        'upcoming_bookings': upcoming_bookings,
        'mock_test_booking': mock_test_booking,
        'on_profile_page': True,
    }

    return render(request, template, context)


def lessons(request):
    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    now = timezone.now()

    """ Gets all bookings made by and associated with the user. """
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
    Gets all bookings with a 'lesson_date' that is
    less than the time now.
    (in the past)
    """
    # Descending Order (Newest to Oldest) displays oldest lessons at bottom
    previous_bookings = profile.bookings.filter(
        models.Q(lesson_date__lt=timezone.now().date()) |
        models.Q(lesson_date=timezone.now().date(), lesson_time__lt=timezone.now().time())
    ).order_by('-lesson_date', '-lesson_time')

    

    """ A view to render the Lessons page. """
    template = 'userprofile/lessons.html'
    context = {
        'profile': profile,
        'all_bookings': all_bookings,
        'upcoming_bookings': upcoming_bookings,
        'previous_bookings': previous_bookings,
        'on_lesson_page': True,
    }

    return render(request, template, context)