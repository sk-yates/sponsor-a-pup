from django.db import models

class Puppy(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name