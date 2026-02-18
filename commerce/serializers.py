from .models import Customer, Order, Remission, Sale, CreditAssignment
from rest_framework import serializers

class CustomerSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Customer
        fields = [ 'id', 'name', 'email', 'is_active' ]

class OrderSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Order
        fields = [ 'id', 'customer', 'folio', 'created_at' ]
        read_only_fields = [ 'created_at']

class RemissionSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Remission
        fields = [ 'id', 'order', 'folio', 'status', 'created_at' ]
        read_only_fields = [ 'created_at' ]

class SaleSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Sale
        fields = [ 'id', 'remission', 'subtotal', 'tax', 'created_at' ]
        read_only_fields = [ 'created_at' ]

class CreditAssignmentSerializer( serializers.ModelSerializer ):
    class Meta:
        model = CreditAssignment
        fields = [ 'id', 'remission', 'amount', 'reason', 'created_at' ]
        read_only_fields = [ 'created_at' ]

