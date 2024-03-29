from rest_framework import serializers
from .models import OrderItem, Order
from product.serializers import ProductSerializer

class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
            "size"
        )
class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many =True)
    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "items",
            "delivery_address",
            "transaction_id",
            "paid_amount",
            "amount_due",
            "delivered",
            "checkoutRequestId",
            "paid"
        )
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
            "size"
        )
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many =True)
    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "items",
            "delivery_address"
        )
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order