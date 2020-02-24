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
from rest_framework.authtoken.views import obtain_auth_token
from bangazonAPI.views import PaymentTypes, ProductTypes
from bangazonAPI.models import PaymentType, ProductType

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'paymenttypes', PaymentTypes, 'paymenttypes')
router.register(r'producttypes', ProductTypes, 'producttypes')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
