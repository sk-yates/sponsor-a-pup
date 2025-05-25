from django.contrib import admin
from .models import SponsorUser, Puppy, Pupdate

#Register your models here.

admin.site.register(Puppy)
admin.site.register(Pupdate)
admin.site.register(SponsorUser)