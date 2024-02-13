from django.shortcuts import render, get_object_or_404
from django.conf import settings

from django.contrib.auth.models import User

from userprofile.models import UserProfile

def index(request):
    user = request.user
    """ Gets all objects associated with the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    """ A view to return the index page """
    template = 'home/index.html'
    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, template, context)
