from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import ProductType

class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttypes',
            lookup_field='id'
        )
        fields = ('id', 'name')
        # customer is not currently a field
        depth = 0

class ProductTypes(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment type instance
        """

        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to payment type resource

        Returns:
            Response -- JSON serialized list of payment types
        """       

        product_types = ProductType.objects.all()

        serializer = ProductTypeSerializer(product_types, many = True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to product type resource

        Returns:
            Response -- JSON serialized detail of deleted product type
        """
        try:
            producttype = ProductType.objects.get(pk=pk)
            producttype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual product type item
        Returns:
            Response -- Empty body with 204 status code
        """
        producttype = ProductType.objects.get(pk=pk)
        producttype.name = request.data["name"]

        producttype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    
    def create(self, request):
        new_producttype = ProductType()
        new_producttype.name = request.data["name"]

        new_producttype.save()

        serializer = ProductTypeSerializer(new_producttype, context={'request': request})

        return Response(serializer.data)