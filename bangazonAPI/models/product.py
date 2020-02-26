from django.db import models
from django.db.models import F
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE
from .customer import Customer
from .product_type import ProductType


class Product(SafeDeleteModel):
    # Objects will be hard-deleted, or soft deleted if other objects would have been deleted too.
    _safedelete_policy = HARD_DELETE_NOCASCADE

    name = models.CharField(max_length=55)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75, null=True)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = (F("created_at").asc(), )

    def __str__(self):
        return self.name
