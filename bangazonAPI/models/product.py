from django.db import models
from django.db.models import F
from .customer import Customer
from .product_type import ProductType


class Product(models.Model):
    name = models.CharField(max_length=55)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75, null=True)
    image_path = models.models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)

    class Meta(self):
        ordering = (F("created_at").desc(), )

    def __str__(self):
        return self.name
