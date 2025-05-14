from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import CreateOrderSerializer, ReadOrderSerializer
from .use_cases import CreateOrderUseCase, OrderData


class CreateOrderView(APIView):
    def post(self, request: Request):
        create_serializer = CreateOrderSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response({'details': create_serializer.errors}, status=400)
        usecase = CreateOrderUseCase()
        order: OrderData = usecase.create_order(
            data=create_serializer.to_order_data()
        )
        read_serializer = ReadOrderSerializer(order)
        return Response({'order': read_serializer.data}, status=201)
