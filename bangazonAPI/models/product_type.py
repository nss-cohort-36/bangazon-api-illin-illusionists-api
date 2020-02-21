from django.db import models
from django.db.models import F


class ProductType(models.Model):
    name = models.CharField(max_length=55)

    class Meta:
        ordering = ("name",)

    def ___str__(self):
        return self.name
