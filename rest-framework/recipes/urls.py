from django.urls import path

from .views import RecipeGetPutDelete, RecipeListCreateView

urlpatterns = [
    path(
        'api/v1/recipes/<int:recipe_id>/',
        RecipeGetPutDelete.as_view(),
        name='recipe-detail-update-delete'
    ),
    path(
        'api/v1/recipes/',
        RecipeListCreateView.as_view(),
        name='recipe-list-create',
    ),
]
