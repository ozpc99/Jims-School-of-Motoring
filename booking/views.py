from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from datetime import datetime, timedelta

from .forms import BookingForm
from .models import Booking
from userprofile.models import UserProfile


# Booking 1/5: The 'bookingPart1' Function
def booking(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    allDates = datesInNext30Days(31)
    availableDates = isDateAvailable(allDates)

    template = 'booking/booking.html'
    context = {
        'profile': profile,
        'allDates': allDates,
        'availableDates': availableDates,
    }

    if request.method == 'POST':
        session_lesson_type = request.POST.get('session_lesson_type')
        session_lesson_date = request.POST.get('session_lesson_date')
        session_house_no = request.POST.get('session_house_no')
        session_street = request.POST.get('session_street')
        session_town = request.POST.get('session_town')
        session_post_code = request.POST.get('session_post_code')

        # Stores in Django session
        request.session['session_lesson_type'] = session_lesson_type
        request.session['session_lesson_date'] = session_lesson_date
        request.session['session_house_no'] = session_house_no
        request.session['session_street'] = session_street
        request.session['session_town'] = session_town
        request.session['session_post_code'] = session_post_code

        # Redirects to BookingPart2 page when form is submitted.
        return redirect('booking_2')

    # Checks if the user profile is complete
    if (
        profile.first_name and
        profile.last_name and
        profile.phone and
        profile.home_house_no and
        profile.home_street and
        profile.home_town and
        profile.home_post_code
    ): 
        return render(request, template, context)
    else:
        messages.warning(request, "Please finish setting up your profile before making a booking.")
        return redirect('profile')


# Booking 2/5: The 'bookingPart2' Function
def booking_2(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user
    timeChoices = ["07:00", "10:00", "13:00", "16:00", "19:00"]
    today = datetime.now()
    minDate = today.strftime('%m-%d-%Y')
    timeDelta = today + timedelta(days=30)
    strTimeDelta = timeDelta.strftime('%m-%d-%Y')
    maxDate = strTimeDelta

    """
    Gets stored data from Django session =>
    - 'lesson_type'
    - 'date'
    - Address details for the meeting point location.
    """
    session_lesson_type = request.session.get('session_lesson_type')
    session_lesson_date = request.session.get('session_lesson_date')
    session_house_no = request.session.get('session_house_no')
    session_street = request.session.get('session_street')
    session_town = request.session.get('session_town')
    session_post_code = request.session.get('session_post_code')

    # Only show times of day that are not already booked.
    timeSlots = isTimeAvailable(timeChoices, session_lesson_date)

    if request.method == 'POST':
        session_lesson_time = request.POST.get('session_lesson_time')

        # Converts session_lesson_time to a string: 'HH:MM'
        session_lesson_time_str = datetime.strptime(session_lesson_time, '%H:%M').strftime('%H:%M')

        if Booking.objects.filter(lesson_date=session_lesson_date).count() < 5: # Allows for 5 bookings to be made on one day. One for each of the 5 time slots.
            if Booking.objects.filter(lesson_date=session_lesson_date, lesson_time=session_lesson_time).count() < 1: # Only 1 booking can be made per time slot on any given day.
                # Store time in Django session.
                request.session['session_lesson_time'] = session_lesson_time
                request.session['session_lesson_time_str'] = session_lesson_time_str
                print(f"session_lesson_time: {session_lesson_time}")
                print(f"session_lesson_time_str: {session_lesson_time_str}")
                print(f"Available time slots: {timeSlots}")
                return redirect('checkout')
            else:
                messages.error(request, "Sorry, that time is unavailable")
        else:
            messages.error(request, "Sorry, that day is fully booked")

    session_lesson_date_object = datetime.strptime(session_lesson_date, '%Y-%m-%d').date()
    session_lesson_date_formatted = session_lesson_date_object.strftime('%a, %d/%m/%y')
    request.session['session_lesson_date_formatted'] = session_lesson_date_formatted

    template = 'booking/booking_2.html'
    context = {
        'profile': profile,
        'timeSlots': timeSlots,
        'session_lesson_type': session_lesson_type,
        'session_lesson_date': session_lesson_date,
        'session_lesson_date_formatted': session_lesson_date_formatted,
        'session_house_no': session_house_no,
        'session_street': session_street,
        'session_town': session_town,
        'session_post_code': session_post_code,
    }

    """ Error handling if lesson date has not been selected """
    if session_lesson_date:
        return render(request, template, context)
    else:
        messages.error(request, "You haven't picked a time")
        return request(('booking_2'))


# Required Functions =>
""" 
Gets the day name from the date and returns a string.
"""
def dayName(x):
    z = datetime.strptime(x, '%Y-%m-%d')
    y = z.strftime('%A')
    return y



def datesInNext30Days(dates):
    """
    Generate a list of dates for the next 30 days from today.
    """
    tomorrow = datetime.now() + timedelta(days=1)
    allDates = [tomorrow + timedelta(days=i) for i in range(30)]
    return allDates



def isDateAvailable(x):
    """
    Checks if date is not already fully booked
    """
    availableDates = []
    for j in x:
        if Booking.objects.filter(lesson_date=j).count() < 4:
            availableDates.append(j)
    return availableDates


def isTimeAvailable(timeChoices, session_lesson_date):
    # Checks if date or time is already booked
    timeSlots = []
    for k in timeChoices:
        if Booking.objects.filter(lesson_date=session_lesson_date, lesson_time=k).count() < 1:
            timeSlots.append(k)
    return timeSlots