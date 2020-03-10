from django.db import models
from django.contrib.auth.models import User 
from django.db.models import F
from bangazonAPI.models import Customer

class Favorite(models.Model):
    current_user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="fuser")
    favorite_user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="fseller")
