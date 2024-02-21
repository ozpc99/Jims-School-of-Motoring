import os

import gspread
from google.oauth2.service_account import Credentials
import json

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.utils.safestring import mark_safe

from django.conf import settings

from django.db import models
from django.db.models import Q

from booking.models import Booking
from booking.forms import BookingForm

from .models import UserProfile
from .forms import *

from datetime import datetime, timedelta

now = datetime.now()
timeZoneNow = timezone.now()

# Profile Page View
@login_required
def profile(request):
    user = request.user
    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    # Welcome Messages
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
                            f'<li class="list-group-item">\
                                <span class="counter me-2">{index + 1}</span>\
                                <span class="fw-bold">{field}</span>\
                            </li>'
                            for index, field in enumerate(incomplete_fields)
                        ]
                    )
                    message = mark_safe(
                        f'<i class="fa-solid fa-circle-info"></i> \
                        <span class="fs-6"> \
                            Please provide the following information: \
                        </span> \
                        <ul class="list-group list-group-flush"> \
                            {incomplete_fields_html} \
                        </ul>'
                    )
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

    """
    Gets all bookings with a 'lesson_date' that is
    greater than or equal to the date now and greater than the time now.
    (today or in the future)

    Excludes cancelled bookings.
    """
    upcoming_bookings = profile.bookings.filter(
        (models.Q(lesson_date__gt=now.date()) |
        (models.Q(lesson_date=now.date(), lesson_time__gt=now.time()))) &
        models.Q(cancelled=False)  # Exclude cancelled bookings
    ).order_by('lesson_date', 'lesson_time')


    """
    Queries the UserProfile booking object for a booking with a 
    lesson_type that matches 'Mock Test'.
    Singles out that specific booking object.
    Finds the latest mock test booking.
    Returns it's associated values. 
    """
    all_bookings = profile.bookings.all()
    def find_mock_test_booking(all_bookings):
        latest_mock_test_date = None
        latest_mock_test = None
        
        for booking in all_bookings:
            if booking.lesson_type == "Mock Test":
                if (latest_mock_test_date is None 
                    or booking.lesson_date > latest_mock_test_date
                ):
                    latest_mock_test_date = booking.lesson_date
                    latest_mock_test = booking
        
        if latest_mock_test:
            return (latest_mock_test.lesson_date,
                    latest_mock_test.lesson_time,
                    latest_mock_test.house_no,
                    latest_mock_test.post_code
                )

    # Assuming all_bookings is defined and populated
    mock_test_booking = find_mock_test_booking(all_bookings)        


    # A view to render the User Profile page.
    template = 'userprofile/profile.html'
    context = {
        'profile': profile,
        'upcoming_bookings': upcoming_bookings,
        'mock_test_booking': mock_test_booking,
        'welcome_message': welcome_message,
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


# Lessons Page View
def lessons(request):
    user = request.user

    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    """ Gets all bookings made by that user """
    all_bookings = profile.bookings.all().order_by(
        'lesson_date', 'lesson_time'
    )

    """
    Gets all bookings with a 'lesson_date' that is
    greater than or equal to the date now and greater than the time now.
    (today or in the future)

    Excludes cancelled bookings.
    """
    upcoming_bookings = profile.bookings.filter(
        (models.Q(lesson_date__gt=now.date()) |
        (models.Q(lesson_date=now.date(), lesson_time__gt=now.time()))) &
        models.Q(cancelled=False)  # Exclude cancelled bookings
    ).order_by('lesson_date', 'lesson_time')

    """
    Gets all bookings with a 'lesson_date' that is
    less than the time now.
    (in the past)
    """
    # Descending Order (Newest to Oldest) displays oldest lessons at bottom
    previous_bookings = profile.bookings.filter(
        (Q(lesson_date__lt=now.date()) |
        (Q(lesson_date=now.date(), lesson_time__lt=now.time())))
    ).order_by('-lesson_date', '-lesson_time')
    

    # Combine booking.lesson_date and booking.lesson_time into a datetime object.
    def lessonDateTime(booking):
        lesson_date = booking.lesson_date
        lesson_time = booking.lesson_time

        lesson_datetime = datetime.combine(lesson_date, lesson_time)
        return lesson_datetime

    # Bookings can be amended or cancelled up to 24h prior to the lesson date and time.
    def isOver24h(booking_reference):
        try:
            booking = Booking.objects.get(booking_reference=booking_reference)
        except Booking.DoesNotExist:
            print('Booking not found.')
            return False

        lesson_datetime = lessonDateTime(booking)
        now = datetime.now()
        delta = lesson_datetime - now

        return delta.total_seconds() > 24 * 60 * 60

    all_bookings = Booking.objects.all()

    editable_bookings = []

    for booking in all_bookings:
        if isOver24h(booking):
            booking.editable = True
            editable_bookings.append(booking)
        else:
            booking.editable = False


    """ A view to render the Lessons page. """
    template = 'userprofile/lessons.html'
    context = {
        'profile': profile,
        'all_bookings': all_bookings,
        'upcoming_bookings': upcoming_bookings,
        'previous_bookings': previous_bookings,
        'editable_bookings': editable_bookings,
        'on_lesson_page': True,
    }
    return render(request, template, context)


# Invoice Page View
def invoice(request, booking_reference):
    profile = get_object_or_404(UserProfile, user=request.user)
    booking = get_object_or_404(Booking, booking_reference=booking_reference)

    template = 'userprofile/invoice.html'
    context = {
        'profile': profile,
        'booking': booking,
    }

    return render(request, template, context)


# Delete Row on Google Sheet
""" Delete Booking Row on Google Sheet """
def delete_row_google_sheet(booking_reference):

    if 'DEVELOPMENT' in os.environ:
        CREDS = Credentials.from_service_account_file('creds.json')
    else:
        credentials = {
            "type": os.environ.get("GOOGLE_SHEETS_TYPE"),
            "project_id": os.environ.get("GOOGLE_SHEETS_PROJECT_ID"),
            "private_key_id": os.environ.get("GOOGLE_SHEETS_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("GOOGLE_SHEETS_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.environ.get("GOOGLE_SHEETS_CLIENT_EMAIL"),
            "client_id": os.environ.get("GOOGLE_SHEETS_CLIENT_ID"),
            "auth_uri": os.environ.get("GOOGLE_SHEETS_AUTH_URI"),
            "token_uri": os.environ.get("GOOGLE_SHEETS_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("GOOGLE_SHEETS_CLIENT_X509_CERT_URL"),
            "universe_domain": os.environ.get("GOOGLE_SHEETS_UNIVERSE_DOMAIN"),
        }
        CREDS = Credentials.from_service_account_info(credentials)

    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('jims_school_of_motoring')

    bookings_worksheet = SHEET.worksheet("bookings")

    booking_cells = bookings_worksheet.findall(booking_reference)

    if booking_cells:
        for cell in booking_cells:
            if cell.value == booking_reference:
                bookings_worksheet.delete_rows(cell.row)
        print(f"Deleted {len(booking_cells)} row(s) associated with {booking_reference}")
    else:
        print(f"No rows found associated with {booking_reference}")


# Cancel Page View
def cancel(request, booking_reference):
    profile = get_object_or_404(UserProfile, user=request.user)
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    user = request.user

    if request.method == 'POST':
        password = request.POST.get('password')
        terms = request.POST.get('terms')

        user = authenticate(request, username=request.user.username, password=password)

        if user is not None:
            if terms:
                booking.cancelled = True
                booking.save()

                delete_row_google_sheet(booking_reference)

                messages.success(request, "Lesson Cancelled!")
                return redirect('lessons')
            else:
                messages.warning(request, "Please accept the terms and conditions")
        else:
            messages.error(request, "Incorrect password")

    template = 'userprofile/cancel.html'
    context = {
        'profile': profile,
        'booking': booking,
    }

    return render(request, template, context)