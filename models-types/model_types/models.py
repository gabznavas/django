from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=255)


class OrderItem(models.Model):
    name = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
