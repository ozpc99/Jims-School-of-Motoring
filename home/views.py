from django.shortcuts import render, get_object_or_404
from django.conf import settings

def index(request):
    username = request.user.username
    print("Username:", username)

    """ A view to return the index page """
    template = 'home/index.html'
    context = {
        'username': username,
    }

    return render(request, template, context)
