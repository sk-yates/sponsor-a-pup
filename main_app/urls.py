from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here

# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in Routes ++++++++++++++++++++++++++
    path('', views.landing, name='landing'),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('signup/email-phone/', views.signup_email_phone, name='signup_email_phone'),
    path('signup/address/', views.signup_address, name='signup_address'),
    path('signup/password/', views.signup_password, name='signup_password'),
    path('signup/pick-pup/', views.signup_pick_pup, name='signup_pick_pup'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('cancel/', views.cancel, name='cancel'),
    path('success/', views.success, name='success'),

# ++++++++++++++++++++++++++ SPONSOR Routes ++++++++++++++++++++++++++
# ------------- Home/Dashboard Routes -------------
    path('home/', views.home, name='home'),

# ------------- User details Routes -------------
    path('my-details/', views.user_details, name='my-details'),

# ------------- Pupdate Routes -------------
    path('pupdates/', views.pupdates, name='pupdates'),
    path('pupdates/<int:pupdate_id>/', views.pupdates_details, name='pupdates-details'),
    
# ------------- Pup details Routes -------------
    path('pup/<int:pup_id>/about/', views.pup_about, name='pup-about'),
    path('pup/<int:pup_id>/videos/', views.pup_videos,name='pup-videos'),
    path('pup/<int:pup_id>/milestones/', views.pup_milestones, name='pup-milestones'),

# ------------- Sponsorship Routes -------------
    path('my-sponsorship/', views.my_sponsorship, name='my-sponsorship'),
    path('my-subscription/', views.my_subscription, name='my-subscription'),


# ++++++++++++++++++++++++++ STAFF Routes ++++++++++++++++++++++++++
# ------------- Pup index Routes -------------
    path('sample-index/', views.sample_pup_index, name='sample-index'),
    path('pup-index/', views.pup_index, name='pup-index'),
    path('pups/<int:pup_id>/', views.pup_profile, name='pup-profile'),
    path('pups/create/', views.PupCreate.as_view(), name='pup-create'),
    path('pups/<int:pk>/update/', views.PupUpdate.as_view(), name='pup-update'),
    path('pups/<int:pk>/delete/', views.PupDelete.as_view(), name='pup-delete'),

]
