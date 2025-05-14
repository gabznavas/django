from django.urls import path

from . import views

urlpatterns = [
    path('order', views.CreateOrderView.as_view(), name='create-order')
]
