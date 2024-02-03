from django.shortcuts import render, get_object_or_404
from django.conf import settings


def profile(request):

    """ A view to return the index page """
    template = 'userprofile/profile.html'
    context = {}

    return render(request, template, context)
