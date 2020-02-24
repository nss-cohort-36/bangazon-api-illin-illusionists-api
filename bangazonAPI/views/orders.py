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
        
        fields = ('id', 'url', 'payment_type_id', 'created_at')
        depth = 0
        
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
        new_order.name = request.data["created_at"]  
        new_order.customer_id = request.auth.user.customer.id
        new_order.save() # saves your instance to the db

        # Pass the new model instance into the serializer, while declaring the context object as request serialized instance
        serializer = AttractionSerializer(newattraction, context={'request': request})
    
    
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

        serializer = OrderSerializer(
            orders,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)
        
        
        
