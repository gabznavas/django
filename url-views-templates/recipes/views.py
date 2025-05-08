from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def home_view(request: HttpRequest):
    return render(request, 'recipes/home.html', context={
        'name': 'John Doe'
    })

def sobre_view(request: HttpRequest):
    return HttpResponse('SOBRE')

def contato_view(request: HttpRequest):
    return HttpResponse('CONTATO')
