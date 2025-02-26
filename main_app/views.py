from django.shortcuts import render

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('Hey, got any dogs!?')

def user_details(request):
    return render(request, 'userdetails.html')

def pupdates(request):
    return render(request, 'pupdates/feed.html', {'pups': pups} )

# views.py

class Pup:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

# Create a list of Cat instances
pups = [
    Pup('Lolo', 'tabby', 'Kinda rude.', 3),
    Pup('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
    Pup('Fancy', 'bombay', 'Happy fluff ball.', 4),
    Pup('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]
