from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('home', views.home, name='home'),
    
    path('my-details/', views.user_details, name='my-details'),
    
    path('pupdates/', views.pupdates, name='pupdates'),
    path('pupdates-details/', views.pupdates_details, name='pupdates-details'),

    path('my-sponsorship/', views.my_sponsorship, name='my-sponsorship'),
    path('my-subscription/', views.my_subscription, name='my-subscription'),


]
