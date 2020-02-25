from django.db import models
from django.db.models import F
from safedelete.models import SafeDeleteModel
from safedelete.models import HARD_DELETE_NOCASCADE
from .customer import Customer

class PaymentType(SafeDeleteModel):
    # Objects will be hard-deleted, or soft deleted if other objects would have been deleted too.
    _safedelete_policy = HARD_DELETE_NOCASCADE

    merchant_name = models.CharField(max_length=25)
    acct_no = models.CharField(max_length=25)
    expiration_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = (F("expiration_date").desc(), )

    def __str__(self):
        return f"{self.merchant_name} ************{self.acct_no[-4: ]}"

