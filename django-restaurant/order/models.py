from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Desk(models.Model):
    deskname = models.CharField(max_length=64)
    price = models.FloatField()
    location = models.CharField(max_length=128)

    def __str__(self):
        return self.deskname


class Meal(models.Model):
    mealname = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return self.mealname


class Order(models.Model):
    orderer = models.ForeignKey(User, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name='orders')
    meal = models.ManyToManyField(Meal, related_name='orders')
    created_time = models.DateTimeField(default=timezone.now)
    sumprice = models.FloatField(default=0)

    def __str__(self):
        return self.created_time.strftime('%Y-%M-%D-%H')
