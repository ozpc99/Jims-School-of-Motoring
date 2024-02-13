from django.shortcuts import render, get_object_or_404
from django.conf import settings

from userprofile.models import UserProfile

def index(request):
    """ A view to return the index page """
    template = 'home/index.html'
    context = {}

    return render(request, template, context)
