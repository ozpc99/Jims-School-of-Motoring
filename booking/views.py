from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from datetime import datetime, timedelta

from .forms import BookingForm
from .models import Booking
from userprofile.models import UserProfile

def booking(request, tab=None):
    today = datetime.now()
    user = request.user
    profile = get_object_or_404(UserProfile, user=request.user)
    
    allDates = datesInNext30Days(30)
    availableDates = isDateAvailable(allDates)
    timeChoices = ["07:00", "10:00", "13:00", "16:00", "19:00"]
    minDate = today.strftime('%m-%d-%Y')
    timeDelta = today + timedelta(days=30)
    strTimeDelta = timeDelta.strftime('%m-%d-%Y')
    maxDate = strTimeDelta

    if request.method == 'POST':
        if 'session_lesson_type' in request.POST:
            session_lesson_type = request.POST.get('session_lesson_type')
            tab = 'meeting-point-tab'
            booking_url = reverse('booking') + f'?tab={tab}'
            return redirect(booking_url)
        elif (
            'session_house_no'
            and 'session_street'
            and 'session_town'
            and 'session_post_code'
        ) in request.POST:
            session_house_no = request.POST.get('session_house_no')
            session_town = request.POST.get('session_town')
            session_street = request.POST.get('session_street')
            session_post_code = request.POST.get('session_post_code')
            tab = 'date-tab'
            booking_url = reverse('booking') + f'?tab={tab}'
            return redirect(booking_url)
        elif 'session_lesson_date' in request.POST:
            session_lesson_date = request.POST.get('session_lesson_date')
            tab = 'time-tab'
            booking_url = reverse('booking') + f'?tab={tab}'
            return redirect(booking_url)
        elif 'session_lesson_time' in request.POST:
            session_lesson_time = request.POST.get('session_lesson_time')
            tab = 'pay-tab'
            booking_url = reverse('booking') + f'?tab={tab}'
            return redirect(booking_url)


    """ A view to return the booking page """
    template = 'booking/booking.html'
    context = {
        'profile': profile,
        'allDates': allDates,
        'availableDates': availableDates,
        'session_lesson_type': request.session.get('session_lesson_type'),
        'session_lesson_date': request.session.get('session_lesson_date'),
        'session_lesson_date_formatted': request.session.get('session_lesson_date_formatted'),
        'session_lesson_time': request.session.get('session_lesson_time'),
        'session_lesson_time_str': request.session.get('session_lesson_time_str'),
        'session_house_no': request.session.get('session_house_no'),
        'session_street': request.session.get('session_street'),
        'session_town': request.session.get('session_town'),
        'session_post_code':request.session.get('session_post_code'),
    }

    """
    Checks if user profile is complete,
    before granting access to booking page.
    """
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