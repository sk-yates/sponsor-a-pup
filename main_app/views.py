from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView

from .models import Puppy

# Import HttpResponse to send text-based responses
from django.http import HttpResponse



# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in ++++++++++++++++++++++++++
class Login(LoginView):
    template_name = 'login.html'

# ++++++++++++++++++++++++++ SPONSOR VIEWS ++++++++++++++++++++++++++
# ------------- Home/Dashboard views -------------
def home(request):
    return render(request, 'dashboard.html')

# ------------- User details views -------------
def user_details(request):
    return render(request, 'userdetails/userdetails.html')

# ------------- Pupdate views -------------
def pupdates(request):
    return render(request, 'pupdates/feed.html', {'pups': sample_pups})

def pupdates_details(request):
    return render(request, 'pupdates/pupdatedetails.html')

# ------------- Sponsorship views -------------
def my_sponsorship(request):
    return render(request, 'sponsorships/mysponsorship.html')

def my_subscription(request):
    return render(request, 'sponsorships/mysubscription.html')


# ++++++++++++++++++++++++++ STAFF VIEWS ++++++++++++++++++++++++++
# ------------- Pup index views -------------
def sample_pup_index(request):
    return render(request, 'pupindex/sampleindex.html', {'pups': sample_pups})

def pup_index(request):
    pups = Puppy.objects.all()
    return render(request, 'pupindex/pupindex.html', {'pups': pups})



# ------------- Pup CRUD views -------------
# C - Create
class PupCreate(CreateView):
    model = Puppy
    template_name = 'main_app/pup_form.html'
    fields = ['name', 'breed', 'age', 'description', 'location']

# R - Read
def pup_profile(request, pup_id):
    pup = Puppy.objects.get(id=pup_id)
    return render(request, 'pupprofiles/pupprofile.html', {'pup': pup})

# U - Update
class PupUpdate(UpdateView):
    model = Puppy
    template_name = 'main_app/pup_form.html'
    fields = ['age', 'description', 'location']

# D - Delete
class PupDelete(DeleteView):
    model = Puppy
    template_name = 'main_app/pup_confirm_delete.html'
    success_url = '/pup-index/'


# ------------- User DB views -------------




















# ------------- Dummy Class and Data -------------

class Sample_pup:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

# Create a list of Cat instances
sample_pups = [
    Sample_pup('Lolo', 'tabby', 'Kinda rude.', 3),
    Sample_pup('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
    Sample_pup('Fancy', 'bombay', 'Happy fluff ball.', 4),
    Sample_pup('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]
