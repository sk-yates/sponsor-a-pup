from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.contrib.auth.hashers import make_password




class SponsorUser(AbstractUser):
    email = models.EmailField(unique=True)
    # groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    pronouns = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_tel = models.CharField(max_length=20)
    contact_pref = models.JSONField(default=list)
    spon_pups = models.ManyToManyField('Puppy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Automatically hash the password on creation if it's not already hashed
        if not self.pk and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Puppy(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField(max_length=500)
    picture_url = models.ImageField(upload_to='puppy_images/', max_length=400, blank=True, null=True)
    location = models.CharField(max_length=100)

    user = models.ManyToManyField(SponsorUser, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pup-profile', kwargs={'pup_id': self.id})


#   # profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

class Pupdate(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=300)
    picture_url = models.ImageField(upload_to='pupdate_images/', max_length=400, blank=True, null=True)
    media_url = models.CharField(max_length=400, blank=True, null=True)
    date = models.DateField('Pupdate date')

    pup = models.ForeignKey(Puppy, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pupdate {self.title} on {self.date}"