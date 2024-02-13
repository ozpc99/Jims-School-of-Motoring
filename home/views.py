from django.shortcuts import render, get_object_or_404
from django.conf import settings

from userprofile.models import UserProfile

def index(request):
    username = request.user.username
    print("Username:", username)
    
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)

    """ A view to return the index page """
    template = 'home/index.html'
    context = {
        'username': username,
        'profile': profile,
    }

    return render(request, template, context)
