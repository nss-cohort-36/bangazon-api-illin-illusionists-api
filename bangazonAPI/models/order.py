from django.db import models
from django.db.models import F
from .payment_type import PaymentType
from .customer import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = (F("created_at").desc(), )

    # def __str__(self):
    #     return 