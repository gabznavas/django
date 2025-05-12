from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import CreateTokenSerializer


class CreateTokenView(APIView):
    def post(self, request: Request):
        try:
            serializer = CreateTokenSerializer(data=request.data)
            valid = serializer.is_valid(raise_exception=False)
            if not valid:
                return Response({
                    "details": serializer.errors
                }, status=400)

            user = User.objects.filter(
                username=serializer.data['email'].strip().lower(),
            ).first()
            if not user:
                return Response({'details': 'e-mail/senha incorretos'})
            if not user.check_password(serializer.data['password']):
                return Response({'details': 'e-mail/senha incorretos'})

            token = RefreshToken()
            refresh = token.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        except Exception as ex:
            print(ex)
            return Response({
                "details": "problema na criacao do token."
            }, status=500)
