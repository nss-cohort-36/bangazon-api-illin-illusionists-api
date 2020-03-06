import json
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from bangazonAPI.models import ProductType
from bangazonAPI.models import Customer


class TestSearch(TestCase):

# Setting up a fake user to use for testing
    def setUp(self):
        self.username = 'testuser'
        self.password = 'secureaf'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.product_type = ProductType.objects.create

    def test_post_product(self):
        # define a product to be sent to the API
        new_product = {
              "name": "Thneed",
              "customer": self.customer.id,
              "price": 12.67,
              "description": "A-fine-something-that-all-people need",
              "quantity": 1,
              "location": "Once-ler's Factory",
              "image_path": "UNLESS.jpg",
              "product_type": self.product_type.id
            }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('parkarea-list'), new_area, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(ParkArea.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(ParkArea.objects.get().name, 'Halloween Land')
