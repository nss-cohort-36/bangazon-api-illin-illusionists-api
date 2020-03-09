import json
import unittest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Product, Customer, ProductType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TestProduct(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foodbar'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

        self.customer = Customer.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name="Wizarding")

    def test_post_product(self):
        # define a product to be sent to the API
        new_product = {
            'name': 'Nimbus 2000',
            'customer': self.customer.id,
            'price': '200.00',
            'description': 'Amazing broomstick',
            'quantity': 24,
            'location': 'Nashville',
            'image_path': 'C:/image.png',
            'created_at': '2019-09-02T14:06:30.047000',
            'product_type_id': 1
        }

        # use the client to send the request and store the response
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        # getting 200 back because we have a success URL
        self.assertEqual(response.status_code, 200)

        # query the table to see if there's one Product instance in there.
        # Since we are testing a POST request, we don't need to test whether an HTTP GET works.
        # So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties.
        self.assertEqual(Product.objects.get().name, 'Nimbus 2000')

        # Let's just check that an extra 0 is not equal
        self.assertNotEqual(Product.objects.get().name, 'Nimbus 20000')

    def test_get_products(self):

        new_product = Product.objects.create(
            name='Nimbus 2000',
            customer_id=self.customer.id,
            price='200.00',
            description='Amazing broomstick',
            quantity=24,
            location='Nashville',
            image_path='C:/image.png',
            created_at='2019-09-02T14:06:30.047000',
            product_type_id=1
        )

        # Now grab all the products (just the one we created) from the db
        response = self.client.get(reverse('product-list'))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST.
        # We already checked that POST works in the previous test (WOO)
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialized data used to render the JSON,
        # while response.content is the JSON itself
        # Are we responidng with the data we asked for? There's just one product
        # in our dummy db, so it should be a list with length = 1
        self.assertEqual(len(response.data), 1)

        # Finally, test the actual rendered content as the client would receive it
        # .encode converts from unicode to utf-8.
        self.assertIn(new_product.name.encode(), response.content)

    def test_get_product(self):

        new_product = Product.objects.create(
            name='Nimbus 2000',
            customer_id=self.customer.id,
            price='200.00',
            description='Amazing broomstick',
            quantity=24,
            location='Nashville',
            image_path='C:/image.png',
            created_at='2019-09-02T14:06:30.047000',
            product_type_id=1
        )

        # Now grab all the products (just the one we created) from the db
        response = self.client.get(reverse('product-detail', kwargs={'pk': 1}))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST.
        # We already checked that POST works in the previous test (WOO)
        self.assertEqual(response.status_code, 200)
        # import pdb; pdb.set_trace()

        self.assertEqual(response.data['name'], new_product.name)

        # response.data is the python serialized data used to render the JSON,
        # while response.content is the JSON itself
        # Are we responidng with the data we asked for? There's just one product
        # in our dummy db, so it should be a list with length = 1
        # self.assertEqual(len(response.data), 1) # doesn't work because I'm only returning object here

        # Finally, test the actual rendered content as the client would receive it
        # .encode converts from unicode to utf-8.
        self.assertIn(new_product.name.encode(), response.content)

        ###
        bad_response = self.client.get(reverse('product-detail', kwargs={'pk': 2}))
        self.assertEqual(bad_response.status_code, 500)

    def test_destroy_product(self):

        new_product = Product.objects.create(
            name='Nimbus 2000',
            customer_id=self.customer.id,
            price='200.00',
            description='Amazing broomstick',
            quantity=24,
            location='Nashville',
            image_path='C:/image.png',
            created_at='2019-09-02T14:06:30.047000',
            product_type_id=1
        )

        # use the client to send the request and store the response
        response = self.client.delete(
            reverse('product-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        # response for successful DELETE
        self.assertEqual(response.status_code, 204)

        # product not in db
        response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(len(response.data), 0)

if __name__ == '__main__':
    unittest.main()
