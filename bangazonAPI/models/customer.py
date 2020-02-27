from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null=True)

    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last = True), )

    # def __str__ (self):
    #     return f'{self.first_name} {self.last_name}'




