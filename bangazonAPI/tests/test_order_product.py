import unittest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Order, OrderProduct, Product, Customer, ProductType, PaymentType
# from .views import <Why don't we need to do this?>


class TestOrderProduct(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.token = Token.objects.create(user=self.user)

        self.customer = Customer.objects.create(user=self.user)

        self.product_type = ProductType.objects.create(name="Gizmo")

        self.payment_type = PaymentType.objects.create(
            merchant_name="Mastercard",
            acct_no="1111111111111111",
            expiration_date="2050-03-05T21:43:09.576Z",
            customer_id=self.customer.id,
            created_at="2020-03-05T21:43:09.576Z")

        self.order = Order.objects.create(
            customer_id=self.customer.id,
            payment_type_id=1,
            created_at="2019-09-23T14:06:30.047Z"
        )
        self.product = Product.objects.create(
            name="The Big Lebowski",
            customer_id=self.customer.id,
            price='9999.99',
            description="That rug really tied the room together",
            quantity=300,
            location="Los Angeles",
            image_path="C:/markitzero.png",
            created_at="2020-03-05T21:43:09.576Z",
            product_type_id=self.product_type.id
        )

    def test_post_order_product(self):
        # define an order, product, and order_product to be sent to the API

        new_order_product = {
            "order_id": self.order.id,
            "product_id": self.product.id
        }

        #  Use the client to send the request and store the response
        response = self.client.post(
            # reverse('orderproduct-list')
            "/orderproducts/cart", new_order_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # Assert
        # Getting 200 back because we have a success url (or a 302 if the view is redirecting )
        self.assertEqual(response.status_code, 200)

#     def test_list_animals(self):

#         # Wait! Why are we saving an Animal instance again?
#         # Aren't we fetching all the animals?
#         # Yes, but...we are not using our actual database for these tests. Your instructor will explain.
#         new_animal = Animal.objects.create(
#         name="Jack",
#         breed="Cocker Spaniel",
#         age= 4,
#         hasShots= True
# )

#         # Now we can grab all the animals (meaning the one we just created) from the db
#         response = self.client.get(reverse('history:animal_list'))

#         # Check that the response is 200 OK.
#         # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
#         self.assertEqual(response.status_code, 200)

#         # Check that the rendered context contains 1 artist.
#         self.assertEqual(len(response.context['animal_list']), 1)

#         # Finally, test the actual rendered content as the browser would receive it
#         # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
#         self.assertIn(new_animal.name.encode(), response.content)
