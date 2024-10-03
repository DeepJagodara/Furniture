# api/models.py

from django.db import models
from django.contrib.auth.models import User

class Furniture(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='furniture_images/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()

    def _str_(self):
        return self.user.username