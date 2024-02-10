from django.shortcuts import render, get_object_or_404
from django.conf import settings


def checkout(request):

    """ A view to return the checkout page """
    template = 'checkout/checkout.html'
    context = {}

    return render(request, template, context)


def success(request):

    """ A view to return the checkout page """
    template = 'checkout/success.html'
    context = {}

    return render(request, template, context)