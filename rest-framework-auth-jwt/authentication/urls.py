from django.urls import path

from .views import CreateTokenView

urlpatterns = [
    path('api/v1/token/', CreateTokenView.as_view(), name="create-token"),
    # path('api/v1/token/', TokenObtainPairView.as_view()),
    # path('api/v1/token/refresh', TokenRefreshView.as_view()),
    # path('api/v1/token/verify', TokenVerifyView.as_view()),
]
