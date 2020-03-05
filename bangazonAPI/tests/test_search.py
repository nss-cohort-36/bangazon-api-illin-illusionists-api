import json
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestSearch(TestCase):

# Setting up a fake user to use for testing
    def setUp(self):
        self.username = 'testuser'
        self.password = 'secureaf'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)