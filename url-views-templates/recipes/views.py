from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def home_view(request: HttpRequest):
    return HttpResponse('HOME')

def sobre_view(request: HttpRequest):
    return HttpResponse('SOBRE')

def contato_view(request: HttpRequest):
    return HttpResponse('CONTATO')
