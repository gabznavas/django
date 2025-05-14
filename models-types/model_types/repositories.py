from django.db import transaction
from .models import Order, OrderItem


class OrderRepository:
    @transaction.atomic
    def create_order(self, data: dict) -> (Order, list[OrderItem]):
        order = Order.objects.create(name=data['name'])
        order_items = []
        for item in data['items']:
            order_item = OrderItem.objects.create(
                name=item.name,
                order=order
            )
            order_items.append(order_item)
        return order, order_items
