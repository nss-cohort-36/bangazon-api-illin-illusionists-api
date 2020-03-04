from django.db import models
from django.db.models import F
from .product import Product
from .order import Order

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="cart")

    class Meta:
        ordering = (F("order").desc(),)