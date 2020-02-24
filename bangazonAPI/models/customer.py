from django.db import models
from django.contrib.auth.models import User
from django.db.models import F


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = (F('user.date_joined').asc(nulls_last = True), )

    def __str__ (self):
        return f'{self.first_name} {self.last_name}'




