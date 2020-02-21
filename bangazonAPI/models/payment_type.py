from django.db import models
from django.db.models import F
from .customer import Customer

class PaymentType(models.Model):
    merchant_name = models.CharField(max_length=25)
    acct_no = models.CharField(max_length=25)
    expiration_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta(self):
        ordering = (F("expiration_date").desc(), )

    def __str__(self):
        return f"{self.merchant_name} ************{self.acct_no[-4: ]}"

