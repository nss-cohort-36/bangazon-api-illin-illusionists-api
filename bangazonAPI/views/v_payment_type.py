from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonAPI.models import PaymentType, Customer

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'acct_no', 'expiration_date', 'customer_id', 'created_at')
        # customer is not currently a field
        depth = 2

class PaymentTypes(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment type instance
        """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to payment type resource

        Returns:
            Response -- JSON serialized list of payment types
        """       

        payment_types = PaymentType.objects.all()

        customer = self.request.query_params.get('customer', None)

        if customer is not None:
            payment_types = payment_types.filter(customer__id=customer)

        serializer = PaymentTypeSerializer(payment_types, many = True, context={'request': request})

        return Response(serializer.data)