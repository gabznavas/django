from dataclasses import dataclass, field
from .repositories import OrderRepository
from .models import Order, OrderItem


@dataclass
class OrderItemData:
    id: int = None
    name: str = ''


@dataclass
class OrderData:
    id: int = None
    name: str = ''
    items: list[OrderItemData] = field(default_factory=list)

    @staticmethod
    def from_validated_data(data: dict) -> "OrderData":
        return OrderData(
            name=data['name'],
            items=[OrderItemData(name=item['name']) for item in data['items']]
        )

    @staticmethod
    def from_order(order: Order, orderItems: list[OrderItem]) -> "OrderData":
        return OrderData(
            id=order.id,
            name=order.name,
            items=[
                OrderItemData(id=item.id, name=item.name)
                for item in orderItems
            ]
        )


class CreateOrderUseCase:

    def __init__(self, order_repository: OrderRepository = None):
        self.order_repository = order_repository or OrderRepository()

    def create_order(self, data: OrderData) -> OrderData:
        (order, order_items) = self.order_repository.create_order({
            "name": data.name,
            "items": data.items
        })
        return OrderData.from_order(order, order_items)
