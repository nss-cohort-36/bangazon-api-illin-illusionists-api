from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import Customer


# class TestUserSerializer(serializers.Serializer):
#     email = serializers.EmailField()

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customers',
            lookup_field='id'
        )

        fields = ('id', 'user')
        # customer is not currently a field
        depth = 4

class Customers(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            customers = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customers,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource

        Returns:
            Response -- JSON serialized list of customers
        """       

        customers = Customer.objects.all()

        # customer = self.request.query_params.get('customer', None)

        # if customer is not None:
        #     payment_types = payment_types.filter(customer__id=customer)

        serializer = CustomerSerializer(customers, many = True, context={'request': request})

        return Response(serializer.data)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests to payment type resource

    #     Returns:
    #         Response -- JSON serialized detail of deleted payment type
    #     """
    #     try:
    #         paymenttype = PaymentType.objects.get(pk=pk)
    #         paymenttype.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except PaymentType.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for an individual payment type item
    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     paymenttype = PaymentType.objects.get(pk=pk)
    #     paymenttype.merchant_name = request.data["merchant_name"]
    #     paymenttype.acct_no = request.data["acct_no"]
    #     paymenttype.expiration_date = request.data["expiration_date"]
    #     paymenttype.customer_id = request.auth.user.customer.id

    #     paymenttype.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    
    # def create(self, request):
    #     new_paymenttype = PaymentType()
    #     new_paymenttype.merchant_name = request.data["merchant_name"]
    #     new_paymenttype.acct_no = request.data["acct_no"]
    #     new_paymenttype.expiration_date = request.data["expiration_date"]
    #     new_paymenttype.customer_id = request.auth.user.customer.id

    #     new_paymenttype.save()

    #     serializer = PaymentTypeSerializer(new_paymenttype, context={'request': request})

    #     return Response(serializer.data)