from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here

# ++++++++++++++++++++++++++ SPONSOR Sign-up/Sign-in Routes ++++++++++++++++++++++++++
    path('', views.Login.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),

# ++++++++++++++++++++++++++ SPONSOR Routes ++++++++++++++++++++++++++
# ------------- Home/Dashboard Routes -------------
    path('home/', views.home, name='home'),

# ------------- User details Routes -------------
    path('my-details/', views.user_details, name='my-details'),

# ------------- Pupdate Routes -------------
    path('pupdates/', views.pupdates, name='pupdates'),
    path('pupdates-details/', views.pupdates_details, name='pupdates-details'),

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
