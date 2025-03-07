from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
# Remove the default User import:
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.hashers import check_password

import stripe

from .forms import SignupNameForm
from .models import Puppy, Pupdate, SponsorUser  # Import SponsorUser instead of User

# Import HttpResponse and JsonResponse to send text-based responses
from django.http import HttpResponse, JsonResponse

#.env this later
YOUR_DOMAIN = "http://localhost:8000"
stripe.api_key = "sk_test_51QxYUHFWIxHlXk0GMXtvmjVBmCBKxzKeyWr5IuoICaE0SB9mBcPvfzBU8YJcS3b8QkFAuxA4947GfFYifYjZprpH00Wk39saOf"

# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in ++++++++++++++++++++++++++
def landing(request):
    return render(request, 'landing.html')

class Login(LoginView):
    template_name = 'login.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = SignupNameForm(request.POST)
        if form.is_valid():
            # Store the name details in the session for later use
            request.session['signup_title'] = form.cleaned_data['title']
            request.session['signup_first_name'] = form.cleaned_data['first_name']
            request.session['signup_last_name'] = form.cleaned_data['last_name']
            # Redirect to the next step: Email & Phone collection
            return redirect('signup_email_phone')
        else:
            error_message = 'Please correct the errors below.'
    else:
        form = SignupNameForm()
    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'signup.html', context)

def signup_email_phone(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if email and phone:
            # Store email and phone in the session
            request.session['signup_email'] = email
            request.session['signup_phone'] = phone
            # Next, collect the address
            return redirect('signup_address')
        else:
            error_message = 'Please provide both your email and phone number.'
    return render(request, 'signup_email_phone.html', {'error_message': error_message})

def signup_address(request):
    error_message = ''
    if request.method == 'POST':
        address = request.POST.get('address')
        if address:
            # Store the address and move to password step
            request.session['signup_address'] = address
            return redirect('signup_password')
        else:
            error_message = 'Please provide your address.'
    return render(request, 'signup_address.html', {'error_message': error_message})

def signup_password(request):
    error_message = ''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            request.session['signup_password'] = password1

            # Retrieve all stored data from the session
            email      = request.session.get('signup_email')
            phone      = request.session.get('signup_phone')
            password   = request.session.get('signup_password')
            address    = request.session.get('signup_address')
            title      = request.session.get('signup_title')
            first_name = request.session.get('signup_first_name')
            last_name  = request.session.get('signup_last_name')

            # Create the SponsorUser (using email as username in this example)
            sponsor_user = SponsorUser.objects.create_user(
                username=email,  # Adjust as needed; ensure create_user is defined
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Optionally, store additional details (title, phone, address) in a profile model

            # Store the new SponsorUser's ID in the session so we can log them in after checkout
            request.session['user_id'] = sponsor_user.id

            # Redirect to the checkout session; user is not logged in until checkout is complete
            return redirect('create-checkout-session')
        else:
            error_message = 'Passwords do not match or were not provided.'
    return render(request, 'signup_password.html', {'error_message': error_message})


def signup_pick_pup(request):
    return render(request, 'signup_pick_pup.html')

def cancel(request) -> HttpResponse:
    return redirect('signup_password')

def success(request) -> HttpResponse:
    user_id = request.session.get('user_id')
    if user_id:
        sponsor_user = SponsorUser.objects.get(pk=user_id)
        login(request, sponsor_user)
        # Clear session data after logging the user in
        request.session.flush()
    return redirect('home')

def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1QzNqBFWIxHlXk0GAJjN0JXF',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + reverse('success'),
            cancel_url=YOUR_DOMAIN + reverse('cancel')
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return redirect(checkout_session.url, code=303)

def custom_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            sponsor_user = SponsorUser.objects.get(email=email)
        except SponsorUser.DoesNotExist:
            error = "Invalid email or password"
        else:
            if check_password(password, sponsor_user.password):
                # Credentials are valid — log the user in
                login(request, sponsor_user)
                # Optionally, store user id in session as well if you need it later:
                request.session['user_id'] = sponsor_user.id
                return redirect('home')
            else:
                error = "Invalid email or password"
    return render(request, 'login.html', {'error': error})

# ++++++++++++++++++++++++++ SPONSOR VIEWS ++++++++++++++++++++++++++
# ------------- Home/Dashboard views -------------
@login_required
def home(request):
    # Retrieve the SponsorUser from the session using the stored id
    user = SponsorUser.objects.get(pk=request.session['user_id'])
    return render(request, 'dashboard.html', {'user': user})


# ------------- User details views -------------
@login_required
def user_details(request):
    return render(request, 'userdetails/userdetails.html')

# ------------- Pupdate views -------------
@login_required
def pupdates(request):
    pupdates = Pupdate.objects.all()
    return render(request, 'pupdates/feed.html', {'pupdates': pupdates})

@login_required
def pupdates_details(request, pupdate_id):
    pupdate = Pupdate.objects.get(id=pupdate_id)
    return render(request, 'pupdates/pupdatedetails.html', {'pupdate': pupdate})


# ------------- Pup details -------------
def pup_about(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_about.html", {"pup": pup})

def pup_videos(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_videos.html", {"pup": pup})

def pup_milestones(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_milestones.html", {"pup": pup})



# ------------- Pup details -------------
def pup_about(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_about.html", {"pup": pup})

def pup_videos(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_videos.html", {"pup": pup})

def pup_milestones(request, pup_id):
    pup = get_object_or_404(Puppy, id=pup_id)
    return render(request, "pupprofiles/pupprofile_milestones.html", {"pup": pup})


# ------------- Sponsorship views -------------
@login_required
def my_sponsorship(request):
    return render(request, 'sponsorships/mysponsorship.html')

@login_required
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
