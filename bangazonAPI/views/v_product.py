"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Product, ProductType

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='products',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'customer_id', 'customer', 'price', 'description','quantity', 'location', 'image_path', 'created_at', 'product_type_id', 'product_type')
        depth = 3

class Products (ViewSet):
    """Products for Bangazon"""
    # handles GET all
    def list(self, request):
        """Handle GET requests for all products

        Returns:
            Response -- JSON serialized product instance
        """
        limit = self.request.query_params.get('limit')
        category = self.request.query_params.get('category', None)
        user = self.request.query_params.get('self')

        location = self.request.query_params.get('location')

        product_name = self.request.query_params.get('name')

        # filter for the 'home' view
        if limit:
            products = Product.objects.order_by('-created_at')[0:int(limit)]
        elif category is not None:
            products = Product.objects.filter(product_type_id=category)
        # filter for the 'myProducts' view
        elif user == "true":
            products = Product.objects.filter(customer_id=request.auth.user.customer.id)
        else:
            products = Product.objects.all()

        # filters for Search
        if location is not None:
            products = products.filter(location = location)

        if product_name is not None:
            products = products.filter(name = product_name)


        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )


        return Response(serializer.data)

    # handles GET one
    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    # Handles POSTs
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        newproduct = Product()
        newproduct.customer_id = request.auth.user.customer.id
        newproduct.name = request.data["name"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.image_path = request.data["image_path"]
        newproduct.product_type_id = request.data["product_type_id"]

        newproduct.save()

        serializer = ProductSerializer(newproduct, context={'request': request})

        return Response(serializer.data)
     # handles DELETE
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            productItem = Product.objects.get(pk=pk)
            # restrict users to only being able to delete products they've created
            if productItem.customer_id == request.auth.user.customer.id:
                productItem.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except productItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# handles PUT
    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
        Response -- Empty body with 204 status code
        """
        productItem = Product.objects.get(pk=pk)      
        productItem.customer_id = request.auth.user.customer.id
        productItem.name = request.data["name"]
        productItem.price = request.data["price"]
        productItem.description = request.data["description"]
        productItem.quantity = request.data["quantity"]
        productItem.location = request.data["location"]
        productItem.image_path = request.data["image_path"]
        productItem.product_type_id = request.data["product_type_id"]
        productItem.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
