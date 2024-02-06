from django.shortcuts import render, get_object_or_404
from django.conf import settings

def index(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Access the username of the user
        username = request.user.username
        # Print the username to the console
        print("Username:", username)
    else:
        # User is not authenticated, set username to None or some default value
        username = None

    """ A view to return the index page """
    template = 'home/index.html'
    context = {
        'username': username,
    }

    return render(request, template, context)
