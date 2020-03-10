from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import OrderProduct, Product, Order, Customer, Favorite
from bangazonAPI.views.v_product import ProductSerializer


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    """
        JSON serializer for favorite

        Arguments:
            serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Favorite
        url = serializers.HyperlinkedIdentityField(
            view_name='favorite',
            lookup_field='id'
        )
        fields = ('id', 'current_user_id', 'favorite_user_id')
        depth = 1


class Favorites(ViewSet):
    """ Order Product Information """

    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Order Product

        Returns:
            Response -- JSON serialized Order Product Instance
        """
        try:
            favorite = Favorite.objects.get(pk=pk)
            serializer = FavoriteSerializer(
                favorite, context={'request', request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Order Product list

        Returns:
            Response -- JSON list of serialized Order Product list
        """

        # get current user id
        current_user_id = request.auth.user.customer.id

        # get favorites by customer user id
        # favorites = Favorite.objects.filter(current_user=current_user_id).select_related('favorite_user__user')
        favorites = Favorite.objects.filter(current_user=current_user_id).values()

        # products = Product.objects.filter(customer_id__in=favorites)[:1]
        

        # get products by favorite user id
        # customer = Customer.objects.filter(id__in=favorites)
        # Model1.objects.extra(where = ['field in (SELECT field from myapp_model2 WHERE ...)'])
        # products = Product.objects.extra(where = ['field in (SELECT * from Product WHERE customer == favorites.favorite_user)'])


        serializer = FavoriteSerializer(
            favorites,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        """
        Handles POST request for Order Product

        Returns:
            Response -- JSON serialized Order Product instance
        """
        new_favorite = Favorite()
        new_favorite.current_user_id = request.auth.user.customer.id
        new_favorite.favorite_user_id = request.data['favorite_user']
          
        new_favorite.save()

        serializer = FavoriteSerializer(new_favorite, context={'request': request})

        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     """
    #     Handles PUT request for Order Product

    #     Returns:
    #         Response -- empty body with 204 status code
    #     """
    #     order_product = Favorite.objects.get(pk=pk)
    #     order_product.order_id = request.data['order_id']
    #     order_product.product_id = request.data['product_id']
    #     order_product.save()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single order product
    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         order_product = Favorite.objects.get(pk=pk)
    #         order_product.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except OrderProduct.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
