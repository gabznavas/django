from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def home(request: HttpRequest):
    dummy_recipes = range(6)
    return render(request, 'recipes/pages/home.html', context={
        "dummy_recipes": dummy_recipes
    })

def recipes(request: HttpRequest, id: int):
    print(id)
    dummy_recipes = range(6)
    return render(request, 'recipes/pages/recipe.html', context={
        "dummy_recipes": dummy_recipes
    })
