from django.db import models
from django.db.models import F
from .product import Product
from .order import Order

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE_DELETE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    class Meta(self):
        ordering = (F("order").desc(),)

    