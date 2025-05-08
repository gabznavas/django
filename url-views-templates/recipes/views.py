from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def home_view(request: HttpRequest):
    return render(request, 'recipes/pages/home.html', context={
        "name": "gabriel navas"
    })
