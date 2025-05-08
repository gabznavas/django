from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpRequest
from recipes.views import home_view, contato_view, sobre_view

urlpatterns = [
    path('', home_view),
    path('sobre/', sobre_view),
    path('contato/', contato_view),
]
