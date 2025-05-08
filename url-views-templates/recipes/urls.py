from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, HttpRequest
from . import views

urlpatterns = [
    path('', views.home),
    path('recipes/<int:id>/', views.recipes),
]
