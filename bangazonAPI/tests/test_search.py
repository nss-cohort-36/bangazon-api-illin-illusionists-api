import json
from django.test import TestCase
from django.urls import reverse
from bangazonAPI.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token