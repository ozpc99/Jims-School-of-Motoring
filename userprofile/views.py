from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models

from django.db.models import Q

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
    hasattr(request.user, 'username') and request.user.username and
    hasattr(request.user, 'email') and request.user.email
    ):
        if not any(
            getattr(profile, field.name)
            for field in profile._meta.fields
            if field.name not in [
                'id', 'user',
                'theory_test_date', 'theory_test_center',
                'mock_test_date',
                'practical_test_date', 'practical_test_center',
            ]
        ):
            messages.info(request, "Please finish setting up your profile.")
        else:
            incomplete_fields = []
            if not profile.first_name:
                incomplete_fields.append("First Name")
            if not profile.last_name:
                incomplete_fields.append("Last Name")
            if not profile.phone:
                incomplete_fields.append("Phone No.")
            if not profile.license_no:
                incomplete_fields.append("Provisional License No.")
            if not profile.license_expiry:
                incomplete_fields.append("Provisional License's Expiry Date")
            if not any(
                getattr(profile, field_name)
                for field_name in [
                    'home_house_no',
                    'home_street',
                    'home_town',
                    'home_post_code',
                ]
            ):
                incomplete_fields.append("Full Home Address")

            if incomplete_fields:
                if len(incomplete_fields) > 1:
                    incomplete_fields_html = ''.join(
                        [
                            f'<li class="list-group-item">{field}</li>'
                            for field in incomplete_fields
                            ]
                    )
                    message = mark_safe(
                        f'<i class="fa-solid fa-circle-info"></i> \
                            <span class="fs-6"> \
                                Please provide the following information: \
                                    </span> \
                                        <ul class="list-group \
                                            list-group-numbered \
                                                list-group-flush"> \
                                                    {incomplete_fields_html} \
                                                        </ul>')
                    messages.info(request, message)
                else:
                    incomplete_fields_html = ''.join(
                        [
                            f'<li class="list-group-item">{field}</li>' 
                            for field in incomplete_fields
                            ]
                    )
                    message = mark_safe(
                        f'<i class="fa-solid fa-circle-info"></i> \
                            <span class="fs-6"> \
                                Please provide the following information: \
                                    </span> \
                                        <ul class="list-group \
                                                list-group-flush"> \
                                                    {incomplete_fields_html} \
                                                        </ul>')
                    messages.info(request, message)
    else:
        messages.error(
            request,
            "Hmm, that's odd. \
                Your profile was not assigned a username or email address \
                    upon registration. Please contact us \
                        and we'll get this fixed."
        )




    # Booking Info:

    """ Gets all bookings made by and associated with the user """
    all_bookings = profile.bookings.all().order_by(
        'lesson_date', 'lesson_time')

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
                return (
                    booking.lesson_date,
                    booking.lesson_time,
                    booking.house_no,
                    booking.post_code
                )
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


""" Update Details Form Handling """
# Name
def update_name(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdateNameForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Name updated successfully')
            return redirect('profile')
        else:
            form = UpdateNameForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)


# Phone Number
def update_phone(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdatePhoneNumberForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone number updated successfully')
            return redirect('profile')
        else:
            form = UpdatePhoneNumberForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)


# Home Address
def update_address(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdateHomeAddressForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Home address updated successfully')
            return redirect('profile')
        else:
            form = UpdateHomeAddressForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)



# License
def update_license(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdateLicenseForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Provisional license details \
                 updated successfully')
            return redirect('profile')
        else:
            form = UpdateLicenseForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)


# Theory Test
def update_theory_test(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdateTheoryTestForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theory test details \
                updated successfully')
            return redirect('profile')
        else:
            form = UpdateTheoryTestForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)


# Practical Test
def update_practical_test(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        form = UpdatePracticalTestForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Practical test details \
                updated successfully')
            return redirect('profile')
        else:
            form = UpdateTheoryTestForm(instance=profile)

    context = {
        'form': form,
    }

    return render(request, 'userprofile/profile.html', context)


def lessons(request):
    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    now = timezone.now()

    """ Gets all bookings made by and associated with the user. """
    all_bookings = profile.bookings.all().order_by(
        'lesson_date',
        'lesson_time'
    )

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
        models.Q(
            lesson_date=timezone.now().date(),
            lesson_time__lt=timezone.now().time()
        )
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