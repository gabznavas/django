from django.urls import path

from . import views

urlpatterns = [
    path('api/recipes/v1', views.recipe_list, name='recipe-list')
]
