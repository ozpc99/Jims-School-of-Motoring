import os

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from booking.forms import BookingForm
from booking.models import Booking
from .models import Price
from userprofile.models import UserProfile

import datetime

import stripe

import gspread
from google.oauth2.service_account import Credentials
import json

# Checkout
""" Cache Booking Data """
@require_POST
def cache_booking_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'save_info': True,
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now, Please try again later.')
        return HttpResponse(content=e, status=400)


""" Post Data to Google Sheet """
def post_to_google_sheet(booking):

    data = {
        'booking_reference': booking.booking_reference,
        'booked_on': booking.booked_on.date(),
        'booked_at': booking.booked_on.time(),
        'full_name': booking.full_name,
        'email': booking.email,
        'lesson_type': booking.lesson_type,
        'lesson_date': booking.lesson_date,
        'lesson_time': booking.lesson_time,
        'house_no': booking.house_no,
        'street': booking.street,
        'town': booking.town,
        'post_code': booking.post_code,
    }

    for key, value in data.items():
        if isinstance(value, datetime.date):
            data[key] = value.strftime("%d/%m/%Y")
        elif isinstance(value, datetime.time):
            data[key] = value.strftime("%H:%M")

    SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

    if 'DEVELOPMENT' in os.environ:
        CREDS = Credentials.from_service_account_file('creds.json')
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
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
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('jims_school_of_motoring')

    print("Updating bookings worksheet...\n")
    bookings_worksheet = SHEET.worksheet("bookings")
    bookings_worksheet.append_row(list(data.values()))
    print("Bookings worksheet updated successfully.\n")


""" Checkout View """
def checkout(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key =  settings.STRIPE_SECRET_KEY
    
    price = Price.get_instance()
    total = price.lesson_price # Get lesson_price from Price model
    stripe_total = round(total * 100)

    stripe.api_key = stripe_secret_key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    print(intent)

    if request.method == 'POST':

        session_lesson_type = request.session.get('session_lesson_type')
        session_lesson_date = request.session.get('session_lesson_date')
        session_lesson_date_formatted = request.session.get('session_lesson_date_formatted')
        session_lesson_time = request.session.get('session_lesson_time')
        session_lesson_time_str = request.session.get('session_lesson_time_str')
        session_house_no = request.session.get('session_house_no')
        session_street = request.session.get('session_street')
        session_town = request.session.get('session_town')
        session_post_code = request.session.get('session_post_code')

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'lesson_type': request.POST['lesson_type'],
            'lesson_date': request.POST['lesson_date'],
            'lesson_time': request.POST['lesson_time'],
            'house_no': request.POST['house_no'],
            'street': request.POST['street'],
            'town': request.POST['town'],
            'post_code': request.POST['post_code'],
            'billpayer_name': request.POST['billpayer_name'],
            'billpayer_house_no': request.POST['billpayer_house_no'],
            'billpayer_street': request.POST['billpayer_street'],
            'billpayer_town': request.POST['billpayer_town'],
            'billpayer_post_code': request.POST['billpayer_post_code'],
        }
        booking_form = BookingForm(form_data)
        
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            pid = intent.client_secret.split('_secret')[0]
            booking.stripe_pid = pid
            booking.save()
            save_info = True

            post_to_google_sheet(booking)

            return redirect(reverse('success', args=[booking.booking_reference]))
        else:
            print(booking_form.errors)
            messages.error(request, 'There was an error with your form \
                Please double check your information.')
            booking_form = BookingForm()

    else:
        session_lesson_type = request.session.get('session_lesson_type')
        session_lesson_date = request.session.get('session_lesson_date')
        session_lesson_date_formatted = request.session.get('session_lesson_date_formatted')
        session_lesson_time = request.session.get('session_lesson_time')
        session_lesson_time_str = request.session.get('session_lesson_time_str')
        session_house_no = request.session.get('session_house_no')
        session_street = request.session.get('session_street')
        session_town = request.session.get('session_town')
        session_post_code = request.session.get('session_post_code')

        booking_form = BookingForm()

    # Helpful debug messages in case stripe keys are not set in env vars
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
        Did you forget to set it in your environment?')

    if not stripe_secret_key:
        messages.warning(request, 'Stripe secret key is missing. \
            Did you forget to set it in your environment?')

    # A view to render the Payment page.
    template = 'checkout/checkout.html'
    context = {
        'profile': profile,
        'booking_form': booking_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'total': total,
        'session_lesson_type': session_lesson_type,
        'session_lesson_date': session_lesson_date,
        'session_lesson_date_formatted': session_lesson_date_formatted,
        'session_lesson_time': session_lesson_time,
        'session_lesson_time_str': session_lesson_time_str,
        'session_house_no': session_house_no,
        'session_street': session_street,
        'session_town': session_town,
        'session_post_code': session_post_code,
    }
    return render(request, template, context)


# Success Page

def success(request, booking_reference):
    """
    Handle Successful Checkouts
    """
    save_info = True
    profile = get_object_or_404(UserProfile, user=request.user)
    booking = get_object_or_404(Booking, booking_reference=booking_reference)

    if 'session_lesson_type' in request.session:
        del request.session['session_lesson_type']

    if 'session_lesson_date' in request.session:
        del request.session['session_lesson_date']

    if 'session_lesson_date_formatted' in request.session:
        del request.session['session_lesson_date_formatted']

    if 'session_lesson_time' in request.session:
        del request.session['session_lesson_time']

    if 'session_lesson_time_str' in request.session:
        del request.session['session_lesson_time_str']

    if 'session_house_no' in request.session:
        del request.session['session_house_no']

    if 'session_street' in request.session:
        del request.session['session_street']

    if 'session_town' in request.session:
        del request.session['session_town']

    if 'session_post_code' in request.session:
        del request.session['session_post_code']

    if request.user.is_authenticated:
        if save_info:
            booking.user_profile = profile
            booking.save()

    messages.success(request, f'Booking successful! \
            Your booking reference number is: {booking.booking_reference} \
            A confirmation email will be sent to: {booking.email}')

    template = 'checkout/success.html'
    context = {
        'booking': booking,
        'profile': profile,
    }

    return render(request, template, context)