from rest_framework import serializers
from .use_cases import OrderData


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()


class CreateOrderSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    items = OrderItemSerializer(many=True)

    def to_order_data(self) -> OrderData:
        return OrderData.from_validated_data(self.validated_data)


class ReadOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    items = OrderItemSerializer(many=True)
