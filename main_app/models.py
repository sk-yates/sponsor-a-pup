from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.urls import reverse

class Puppy(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pup-profile', kwargs={'pup_id': self.id})
    
class User(models.Model):
    user_email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
    pronouns = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_tel = models.CharField(max_length=20)
    contact_pref = models.JSONField(default=list)
    spon_pups = models.ManyToManyField('Puppy')
    created_at = models.DateTimeField(auto_now_add=True)
