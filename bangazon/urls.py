"""bangazon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from bangazonAPI.views import Customers, Users, Products, OrderProducts, PaymentTypes, ProductTypes, Orders, register_user, login_user
from rest_framework.authtoken.views import obtain_auth_token
from bangazonAPI.models import *
from django.contrib.auth.models import User

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'orderproducts', OrderProducts, 'orderproduct')
router.register(r'orders', Orders, 'order')
router.register(r'products', Products, 'product')
router.register(r'paymenttypes', PaymentTypes, 'paymenttype')
router.register(r'producttypes', ProductTypes, 'producttype')
router.register(r'customers', Customers, 'customer')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('admin', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
