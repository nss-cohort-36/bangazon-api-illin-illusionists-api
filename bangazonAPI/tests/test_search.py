import json
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from bangazonAPI.models import ProductType
from bangazonAPI.models import Customer
from unittest import skip


class TestSearch(TestCase):

# Setting up a fake user and foreign keys to use for testing
    def setUp(self):
        self.username = 'testuser'
        self.password = 'secureaf'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user)
        self.product_type = ProductType.objects.create(name="Test Object")
    
    # POST PRODUCT
    def test_post_product(self):
        # define a product to be sent to the API
        new_product = {
              "name": "Thneed",
              "customer": self.customer.id,
              "price": 12.67,
              "description": "A fine something that all people need",
              "quantity": 1,
              "location": "Once-ler's Factory",
              "image_path": "UNLESS.jpg",
              "product_type_id": self.product_type.id
            }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )


        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one Product instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Product.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Product.objects.get().name, 'Thneed')
    
    # GET PRODUCT BY NAME
    def test_get_products_by_name(self):
        new_product = Product.objects.create(
              name = "Thneed",
              customer_id = self.customer.id,
              price = 12.67,
              description = "A fine something that all people need",
              quantity = 1,
              location = "Once-ler's Factory",
              image_path = "UNLESS.jpg",
              product_type_id = self.product_type.id
        )

        name = "Thneed"
        # Now we can grab all the products (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list') + f'?name={name}')

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Thneed")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.name.encode(), response.content)

# GET PRODUCT BY LOCATION
    def test_get_products_by_location(self):
        new_product = Product.objects.create(
              name = "Thneed",
              customer_id = self.customer.id,
              price = 12.67,
              description = "A fine something that all people need",
              quantity = 1,
              location = "Once-ler's Factory",
              image_path = "UNLESS.jpg",
              product_type_id = self.product_type.id
        )

        location = "Once-ler's Factory"
        # Now we can grab all the products (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list') + f'?location={location}')

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["location"], "Once-ler's Factory")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.name.encode(), response.content)

# GET PRODUCT BY NAME AND LOCATION
    def test_get_products_by_name_and_location(self):
        new_product = Product.objects.create(
              name = "Thneed",
              customer_id = self.customer.id,
              price = 12.67,
              description = "A fine something that all people need",
              quantity = 1,
              location = "Once-ler's Factory",
              image_path = "UNLESS.jpg",
              product_type_id = self.product_type.id
        )

        name = "Thneed"
        location = "Once-ler's Factory"
        # Now we can grab all the products (meaning the one we just created) from the db
        response = self.client.get(reverse('product-list') + f'?name={name}&location={location}')

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one product in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["name"], "Thneed")

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["location"], "Once-ler's Factory")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_product.name.encode(), response.content)

if __name__ == '__main__':
    unittest.main()