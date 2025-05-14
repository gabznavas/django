from dataclasses import dataclass

from django.urls import path

from .views import CreateAndFindAllUserView


@dataclass
class UrlNames:
    CREATE_AND_FIND_ALL_USERS = "create_and_find_all_users"


urlpatterns = [
    path('api/v1/users/', CreateAndFindAllUserView.as_view(), name=UrlNames.CREATE_AND_FIND_ALL_USERS),
]
