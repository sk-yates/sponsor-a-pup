from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.hashers import check_password
from django.urls import reverse
import stripe
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .decorators import anonymous_required
from .forms import SignupNameForm, PuppyForm, PupdateForm
from .models import Puppy, Pupdate, SponsorUser  # Import SponsorUser instead of User

from django.http import HttpResponse, JsonResponse

# In production, load these values from environment variables.
YOUR_DOMAIN = "http://localhost:8000"
stripe.api_key = "sk_test_51QxYUHFWIxHlXk0GMXtvmjVBmCBKxzKeyWr5IuoICaE0SB9mBcPvfzBU8YJcS3b8QkFAuxA4947GfFYifYjZprpH00Wk39saOf"  # Your Stripe secret key

# ++++++++++++++++++++++++++ STRIPE Webhook ++++++++++++++++++++++++++

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # Set this in your settings/.env file

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event based on its type
    if event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        # Process the subscription created event (e.g., mark subscription as active in your database)
        # Example: update_subscription_status(subscription, 'active')
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        # Process the subscription updated event (e.g., update details in your database)
        # Example: update_subscription_status(subscription, 'updated')
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Process the subscription cancelled event
        # Example: update_subscription_status(subscription, 'cancelled')
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)

# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in ++++++++++++++++++++++++++

@anonymous_required
def landing(request):
    return render(request, 'landing.html')

class Login(LoginView):
    template_name = 'login.html'

@anonymous_required
def create_checkout_session(request):
    # Capture the selected pup from the query parameters, if present
    selected_pup = request.GET.get('selected_pup')
    if selected_pup:
        request.session['selected_pup'] = selected_pup

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["bacs_debit"],
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

@anonymous_required
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

@anonymous_required
def signup_address(request):
    # Collects address details
    error_message = ''
    if request.method == 'POST':
        address = request.POST.get('address')
        contact_pref = request.POST.getlist('contact_pref')
        if address:
            request.session['signup_address'] = address
            request.session['contact_pref'] = contact_pref
            # Redirect to the next step: Email & Phone collection
            return redirect('signup_email_phone')
        else:
            error_message = 'Please provide your address and contact preferences.'
    return render(request, 'signup_address.html', {'error_message': error_message})

@anonymous_required
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

@anonymous_required
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
            contact_pref = request.session.get('contact_pref', [])

             # Create a Stripe Customer
            stripe_customer = stripe.Customer.create(
                email=email,
                name=f"{first_name} {last_name}"
            )

            # Create the SponsorUser (using email as username)
            sponsor_user = SponsorUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                stripe_customer_id=stripe_customer.id,
                contact_pref=contact_pref
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

@anonymous_required
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
    
    # Render the template and set no-cache headers
    response = render(request, 'login.html', {'error': error})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# ++++++++++++++++++++++++++ SPONSOR VIEWS ++++++++++++++++++++++++++
@login_required
def home(request):
    response = render(request, 'dashboard.html', {'user': request.user})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# ------------- User details views -------------
@login_required
def user_details(request):
    return render(request, 'userdetails/userdetails.html')

# ------------- Pupdate views -------------
@login_required
@permission_required('main_app.can_view_all_elements', raise_exception=True)
def pupdates(request):
    pupdates = Pupdate.objects.all()
    print(f"Retrieved {pupdates.count()} pupdates")  # Debugging statement
    for pupdate in pupdates:
        print(f"Pupdate ID: {pupdate.id}, Title: {pupdate.title}")  # Debugging statement
    return render(request, 'pupdates/feed.html', {'pupdates': pupdates})

@login_required
def feed_view(request):
    user = request.user
    pupdates = Pupdate.objects.filter(pup__user=user)
    print(f"User: {user.username}, Pupdates: {pupdates}") # Debugging
    return render(request, 'pupdates/feed_view.html', {'pupdates': pupdates})

@login_required
def pupdates_details(request, pupdate_id):
    pupdate = Pupdate.objects.get(id=pupdate_id)
    return render(request, 'pupdates/pupdatedetails.html', {'pupdate': pupdate})


# ------------- Pupdate CRUD views -------------
class PupdateCreate(CreateView):
    model = Pupdate
    form_class = PupdateForm
    template_name = 'pupdates/pupdate_form.html'
    success_url = '/pupdates/'

class PupdateUpdate(UpdateView):
    model = Pupdate
    template_name = 'pupdates/pupdate_form.html'
    fields = ['title', 'content', 'picture_url', 'media_url', 'date']
    success_url = '/pupdates/'

class PupdateDelete(DeleteView):
    model = Pupdate
    template_name = 'pupdates/pupdate_confirm_delete.html'
    success_url = '/pupdates/'


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
    stripe_customer_id = request.user.stripe_customer_id
    if not stripe_customer_id:
        return HttpResponse("Stripe customer not found.", status=400)
    
    try:
        portal_session = stripe.billingPortal.Session.create(
            customer=stripe_customer_id,
            return_url=YOUR_DOMAIN + reverse('home'),
        )
    except Exception as e:
        return HttpResponse(f"Error creating portal session: {e}", status=500)
    
    return redirect(portal_session.url, code=303)


# ++++++++++++++++++++++++++ STAFF VIEWS ++++++++++++++++++++++++++
# ------------- Pup index views -------------
def sample_pup_index(request):
    return render(request, 'pupindex/sampleindex.html', {'pups': sample_pups})

@permission_required('main_app.can_view_all_elements', raise_exception=True)
def pup_index(request):
    pups = Puppy.objects.all()
    print(pups)
    return render(request, 'pupindex/pupindex.html', {'pups': pups})

# xaiver pick up pup code
def signup_pick_pup(request):
    pups = Puppy.objects.filter(is_sponsorable=True)  # Filter by is_sponsorable for only sponsorable pups
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
    form_class = PuppyForm
    template_name = 'main_app/pup_form.html'

# R - Read
def pup_profile(request, pup_id):
    pup = Puppy.objects.get(id=pup_id)
    return render(request, "pupprofiles/pupprofile.html", {"pup": pup})

# U - Update
class PupUpdate(UpdateView):
    model = Puppy
    template_name = 'main_app/pup_form.html'
    fields = ['name', 'breed', 'age', 'description', 'picture_url', 'location', 'user']

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
