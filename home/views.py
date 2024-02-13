from django.shortcuts import render, get_object_or_404
from django.conf import settings

from django.contrib.auth.models import User

from userprofile.models import UserProfile

def index(request):
    # Checks if user is authenticated
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
    else:
        profile = None

    """ A view to return the index page """
    template = 'home/index.html'
    context = {
        'user': request.user,
        'profile': profile,
    }

    return render(request, template, context)
