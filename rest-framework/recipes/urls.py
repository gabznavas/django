from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/recipes/', views.recipe_list, name='recipe-list'),
    path('api/v1/recipes/<int:id>', views.recipe_detail, name='recipe-detail'),
]
