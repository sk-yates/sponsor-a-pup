from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse
from django.contrib.auth.hashers import make_password

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
    

class SponsorUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    pronouns = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_tel = models.CharField(max_length=20)
    contact_pref = models.JSONField(default=list)
    spon_pups = models.ManyToManyField('Puppy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# # class User(models.Model):
#     user_email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
#     pronouns = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     user_tel = models.CharField(max_length=20)
#     contact_pref = models.JSONField(default=list)
#     spon_pups = models.ManyToManyField('Puppy')
#     created_at = models.DateTimeField(auto_now_add=True)
    # is_seller = models.BooleanField(default=False)
    # profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)


#     def save(self, *args, **kwargs):
#         # Automatically hash the password on creation if it's not already hashed
#         if not self.pk and not self.password.startswith('pbkdf2_'):
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)