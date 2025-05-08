from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def home_view(request: HttpRequest):
    dummy_recipes = range(6)
    return render(request, 'recipes/pages/home.html', context={
        "dummy_recipes": dummy_recipes
    })
