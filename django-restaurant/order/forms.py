from django import forms

from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('desk', 'meal')


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('mealname','price')


class DeskForm(forms.ModelForm):
    class Meta:
        model = Desk
        fields = ('deskname', 'location', 'price')