from django.urls import path

from .views import CreateAndFindAllUserView

urlpatterns = [
    path('api/v1/users/', CreateAndFindAllUserView.as_view(), name="create-and-find-all-users"),
]
