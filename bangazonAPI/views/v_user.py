from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        
        fields = ('id', 'username','first_name', 'last_name', 'email')
        # customer is not currently a field
        # depth = 2

class Users(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """

        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource

        Returns:
            Response -- JSON serialized list of customers
        """       

        users = User.objects.all()

        # customer = self.request.query_params.get('customer', None)

        # if customer is not None:
        #     payment_types = payment_types.filter(customer__id=customer)

        serializer = UserSerializer(users, many = True, context={'request': request})

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

    def partial_update(self, request, pk=None):
        """Handle PATCH requests for a customer
        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]

        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    
    # def create(self, request):
    #     new_paymenttype = PaymentType()
    #     new_paymenttype.merchant_name = request.data["merchant_name"]
    #     new_paymenttype.acct_no = request.data["acct_no"]
    #     new_paymenttype.expiration_date = request.data["expiration_date"]
    #     new_paymenttype.customer_id = request.auth.user.customer.id

    #     new_paymenttype.save()

    #     serializer = PaymentTypeSerializer(new_paymenttype, context={'request': request})

    #     return Response(serializer.data)