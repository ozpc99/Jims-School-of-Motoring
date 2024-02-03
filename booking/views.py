from django.shortcuts import render, get_object_or_404
from django.conf import settings


def booking(request):

    """ A view to return the booking page """
    template = 'booking/booking.html'
    context = {}

    return render(request, template, context)
