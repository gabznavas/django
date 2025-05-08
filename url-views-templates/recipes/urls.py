from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpRequest
from recipes.views import home_view

urlpatterns = [
    path('', home_view),
]
