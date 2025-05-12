from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer, ReadUserSerializer


class CreateAndFindAllUserView(APIView):
    def get(self, _: Request):
        try:
            user = User.objects.all()
            serializer = ReadUserSerializer(user, many=True)

            return Response({
                "data": serializer.data
            })
        except Exception as ex:
            print(ex)
            return Response({
                "details": "problema na busca de todos os usuários."
            }, status=500)

    def post(self, request: Request):
        try:
            serializer = CreateUserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"details": serializer.errors}, status=400)

            user = User.objects.filter(email=serializer.validated_data['email']).first()
            if user:
                return Response({
                    "details": "e-mail já está em uso."
                }, status=400)

            user = User()
            user.first_name = serializer.validated_data['first_name'].strip()
            user.last_name = serializer.validated_data['last_name'].strip()
            user.email = serializer.validated_data['email'].strip().lower()
            user.username = serializer.validated_data['email'].strip().lower()
            user.set_password(serializer.validated_data['password'])
            user.save()

            read_serializer = ReadUserSerializer(instance=user)
            return Response({"data": read_serializer.data}, status=201)

        except Exception as ex:
            print(ex)
            return Response({
                "details": "problema na criação do usuário."
            }, status=500)
