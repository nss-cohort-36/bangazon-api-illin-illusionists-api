from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Order, PaymentType, Customer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
        JSON serializer for Orders
        
        Arguments:
            serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order',
            lookup_field = 'id'
        )
        
        fields = ('id', 'url','customer_id','customer', 'payment_type_id', 'payment_type', 'created_at', 'cart')
        depth = 3
        
class Orders(ViewSet):
    """Orders view for Bangazon API"""
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Order instance
        """
        # Start by creating a new instance of the Order model
        new_order = Order()
        # The request.data["str"] expression evaluates the key names from your models and saves those values in your new model instance.
        new_order.customer_id = request.auth.user.customer.id
        new_order.payment_type_id = request.data["payment_type"]  
        new_order.save() # saves your instance to the db

        # Pass the new model instance into the serializer, while declaring the context object as request serialized instance
        serializer = OrderSerializer(new_order, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_to_delete = Order.objects.get(pk=pk)
            order_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except order_to_delete.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            single_order_record = Order.objects.get(pk=pk)
            serializer = OrderSerializer(single_order_record, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    
    # ! Ask why this one doesn't work but the other one does with a different naming convention
    # def retrieve(self, request, pk=None):
    #     """Handles the GET request for a single order
        
    #     Returns:
    #         -- A JSON serialized response object
    #     """
        
    #     try:
    #         # Store a ref to the specific resource in a variable
    #         order = Order.objects.get(pk=pk) # Call .objects on the model
    #         # Serialize the response and store it in a variable
    #         serializer = OrderSerializer(order, context={'request', request})
    #         # Return the serialized response object
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)
        
    def list(self, request):
        """Handles a GET request for all orders
        
        Returns:
            A serialized list of all orders
        """

        # Get all instances of orders from the db and store in the orders variable
        orders = Order.objects.all()

        customer_only = request.query_params.get('self', False)
        open_order = request.query_params.get('open', False)

        if customer_only == 'true':
          orders = orders.filter(customer__id=request.auth.user.customer.id)
        
        if open_order == 'true':
          orders = orders.filter(payment_type__id=None)

        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)
        
        
        
    def patch(self, request, pk=None):
        """Handle PATCH requests for an individual order item
           to update only the payment_type
        Returns:
            Response -- Empty body with 204 status code
        """
        updated_order = Order.objects.get(pk=pk)
        updated_order.payment_type_id = request.data["payment_type"]  

        updated_order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
