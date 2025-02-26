from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path('', views.home, name='home'),
    path('my-details/', views.user_details, name='my-details'),
    path('pupdates/', views.pupdates, name='pupdates'),
]
