from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from utils.recipes.factory import make_recipe

def home(request: HttpRequest):
    dummy_recipes = range(6)
    return render(request, 'recipes/pages/home.html', context={
        "recipes": [make_recipe() for _ in range(10)]
    })

def recipes(request: HttpRequest, id: int):
    print(id)
    dummy_recipes = range(6)
    return render(request, 'recipes/pages/recipe.html', context={
        "recipe": make_recipe()
    })
