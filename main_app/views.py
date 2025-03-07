from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.hashers import check_password
import stripe

from .forms import SignupNameForm
from .models import Puppy, Pupdate, SponsorUser

from django.http import HttpResponse, JsonResponse

# In production, load these values from environment variables.
YOUR_DOMAIN = "http://localhost:8000"
stripe.api_key = "sk_test_51QxYUHFWIxHlXk0GMXtvmjVBmCBKxzKeyWr5IuoICaE0SB9mBcPvfzBU8YJcS3b8QkFAuxA4947GfFYifYjZprpH00Wk39saOf"  # Your Stripe secret key

# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in ++++++++++++++++++++++++++

def landing(request):
    return render(request, 'landing.html')

class Login(LoginView):
    template_name = 'login.html'

def create_checkout_session(request):
    # Capture the selected pup from the query parameters, if present
    selected_pup = request.GET.get('selected_pup')
    if selected_pup:
        request.session['selected_pup'] = selected_pup

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
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

def success(request) -> HttpResponse:
    # After checkout, redirect to the signup flow.
    return redirect('signup')

def signup(request):
    # Collects name details
    error_message = ''
    if request.method == 'POST':
        form = SignupNameForm(request.POST)
        if form.is_valid():
            request.session['signup_title'] = form.cleaned_data['title']
            request.session['signup_first_name'] = form.cleaned_data['first_name']
            request.session['signup_last_name'] = form.cleaned_data['last_name']
            # Redirect to the next step: Address collection
            return redirect('signup_address')
        else:
            error_message = 'Please correct the errors below.'
    else:
        form = SignupNameForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def signup_address(request):
    # Collects address details
    error_message = ''
    if request.method == 'POST':
        address = request.POST.get('address')
        if address:
            request.session['signup_address'] = address
            # Redirect to the next step: Email & Phone collection
            return redirect('signup_email_phone')
        else:
            error_message = 'Please provide your address.'
    return render(request, 'signup_address.html', {'error_message': error_message})

def signup_email_phone(request):
    # Collects email and phone details
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if email and phone:
            request.session['signup_email'] = email
            request.session['signup_phone'] = phone
            # Redirect to the next step: Password collection
            return redirect('signup_password')
        else:
            error_message = 'Please provide both your email and phone number.'
    return render(request, 'signup_email_phone.html', {'error_message': error_message})

def signup_password(request):
    # Collects password, creates the SponsorUser, and completes the signup flow.
    error_message = ''
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            request.session['signup_password'] = password1

            # Retrieve all stored signup data from the session
            email      = request.session.get('signup_email')
            phone      = request.session.get('signup_phone')
            password   = request.session.get('signup_password')
            address    = request.session.get('signup_address')
            title      = request.session.get('signup_title')
            first_name = request.session.get('signup_first_name')
            last_name  = request.session.get('signup_last_name')

            # Create the SponsorUser (using email as username)
            sponsor_user = SponsorUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Optionally, store additional details (like title, phone, address) via a profile model

            # Log in the user
            login(request, sponsor_user)
            return redirect('home')
        else:
            error_message = 'Passwords do not match or were not provided.'
    return render(request, 'signup_password.html', {'error_message': error_message})

def cancel(request) -> HttpResponse:
    return redirect('signup_password')

def custom_login(request):
    # Standard login for existing users
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
                login(request, sponsor_user)
                return redirect('home')
            else:
                error = "Invalid email or password"
    return render(request, 'login.html', {'error': error})

# ++++++++++++++++++++++++++ SPONSOR VIEWS ++++++++++++++++++++++++++
@login_required
def home(request):
    return render(request, 'dashboard.html', {'user': request.user})

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



# xaiver pick up pup code
def signup_pick_pup(request):
    pups = Puppy.objects.all()  # Fetch all puppies from the database
    return render(request, "signup_pick_pup.html", {"pups": pups})

def pup_profile_redirect(request):
    if request.method == "POST":
        selected_pup_id = request.POST.get("selected_pup")  # Get pup ID as a string
        if selected_pup_id and selected_pup_id.isdigit():  # Ensure it's a number
            return redirect("pup-profile", pup_id=int(selected_pup_id))  # Convert to integer
    return redirect("signup-pick-pup")  # Redirect back if no selection

# ------------- Pup CRUD views -------------
# C - Create
class PupCreate(CreateView):
    model = Puppy
    template_name = 'main_app/pup_form.html'
    fields = ['name', 'breed', 'age', 'description', 'location']

# R - Read
def pup_profile(request, pup_id):
    pup = Puppy.objects.get(id=pup_id)
    return render(request, "pupprofiles/pupprofile.html", {"pup": pup})

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
