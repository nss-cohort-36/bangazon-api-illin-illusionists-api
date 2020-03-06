import json
import datetime
from django.utils.timezone import make_aware
from django.conf import settings

from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Order
from bangazonAPI.models import Customer
from bangazonAPI.models import PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TestOrder(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

        self.customer = Customer.objects.create(user=self.user)

        settings.TIME_ZONE
        naive_datetime = datetime.datetime.now()
        aware_datetime = make_aware(naive_datetime)

        self.payment_type = PaymentType.objects.create(
            merchant_name="'Murican Express",
            acct_no="1234567890123456",
            expiration_date=aware_datetime,
            customer_id=self.customer.id
        )

        self.new_order = Order.objects.create(customer_id=self.customer.id)

    def test_retrieve_order(self):
        response = self.client.get(
            (reverse('order-detail', kwargs={'pk': self.new_order.id})), HTTP_AUTHORIZATION='Token ' + str(self.token),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.get().payment_type_id, None)

    def test_patch_order(self):
        updated_order = {
            "payment_type": self.payment_type.id,
        }

        response = self.client.patch(
            reverse('order-detail', kwargs={'pk': self.new_order.id}), updated_order, HTTP_AUTHORIZATION='Token ' + str(self.token),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)

        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.get().payment_type_id, 1)
