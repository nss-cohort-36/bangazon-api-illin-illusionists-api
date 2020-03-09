from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import OrderProduct, Product, Order, Customer
from django.db.models import Sum, Count


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """
        JSON serializer for order products

        Arguments:
            serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'order', 'product_id', 'product')
        depth = 3


class OrderProducts(ViewSet):
    """ Order Product Information """

    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Order Product

        Returns:
            Response -- JSON serialized Order Product Instance
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request', request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Order Product list

        Returns:
            Response -- JSON list of serialized Order Product list
        """

        product_id = request.query_params.get('product')
        order_id = request.query_params.get('order', None)
        open_order_products = request.query_params.get('open_order_products', None)

        if product_id:
            order_products = OrderProduct.objects.filter(product_id=product_id)
        elif order_id is not None:
            order_products = OrderProduct.objects.filter(order__id=order_id)
        elif open_order_products == "true":
            order_products = OrderProduct.objects.filter(order__payment_type=None).annotate(Count('product_id')).values('product_id').order_by()
                # .aggregate(Count('order_id'))
        else:
            order_products = OrderProduct.objects.all()


        serializer = OrderProductSerializer(
            order_products,
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
        new_order_product = OrderProduct()
        new_order_product.order_id = request.data['order_id']
        new_order_product.product_id = request.data['product_id']

        new_order_product.save()

        serializer = OrderProductSerializer(new_order_product, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Handles PUT request for Order Product

        Returns:
            Response -- empty body with 204 status code
        """
        order_product = OrderProduct.objects.get(pk=pk)
        order_product.order_id = request.data['order_id']
        order_product.product_id = request.data['product_id']
        order_product.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order product
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def cart(self, request):
        current_user = Customer.objects.get(user=request.auth.user.customer.id)

        try:
            open_order = Order.objects.get(
                customer=current_user, payment_type=None)

        except Order.DoesNotExist:
            open_order = Order()
            open_order.customer_id = request.auth.user.customer.id
            # open_order.payment_type = None
            open_order.save()

        new_order_product = OrderProduct()
        new_order_product.order_id = open_order.id
        new_order_product.product_id = request.data['product_id']
        new_order_product.save()

        serializer = OrderProductSerializer(
            new_order_product, context={'request': request})

        return Response(serializer.data)
   
   