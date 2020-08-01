from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import *
from .forms import *

# Create your views here.

def home(request):
    try:
        user = User.objects.get(id=request.user.id)       
        context = {'user': user} 
        return render(request, 'home.html', context)
    except:
        return render(request, 'home.html')


class DeskListView(ListView):
    model = Desk
    context_object_name = 'desks'
    template_name = 'desklist.html'


class MealListView(ListView):
    model = Meal
    context_object_name = 'meals'
    template_name = 'meallist.html'


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'orderlist.html'


@login_required
def neworder(request):
    if request.method == 'POST':
        newform = OrderForm(request.POST)
        if newform.is_valid():
            new_order = newform.save(commit=False)
            new_order.orderer = User.objects.get(id=request.user.id)
            if request.POST['desk'] != 'none':
                new_order.desk = Desk.objects.get(id=request.POST['desk'])
            new_order.save()           
            return redirect('order:orderlist')
        else:
            return HttpResponse('Form Wrong !')
    else:
        newform = OrderForm()
        desks = Desk.objects.all()
        meals = Meal.objects.all()
        context = {'newform': newform, 'desks': desks, 'meals': meals} 

        return render(request, 'neworder.html', context)


@login_required
def newmeal(request):  
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MealForm(request.POST)
            if form.is_valid():
                new_meal = form.save()
                return redirect('order:meallist')
            else:
                return HttpResponse('Wrong Meal')
        else:
            form = MealForm()
            return render(request, 'meallist.html')
    else:
        return HttpResponse('Only the Restaurant keeper can manage the Meal list !')


@login_required
def newdesk(request):  
    if request.user.is_superuser:
        if request.method == 'POST':
            form = DeskForm(request.POST)
            if form.is_valid():
                new_desk = form.save()     
                return redirect('order:desklist')
            else:
                return HttpResponse('Wrong Desk')
        else:
            form = DeskForm()
            return render(request, 'desklist.html')
    else:
        return HttpResponse('Only the Restaurant keeper can manage the Desk list !')


@login_required
def deleteorder(request, id):  
    if request.user.is_superuser:
        order = Order.objects.get(id=id)
        order.delete()
        return redirect('order:orderlist')
    else:
        return HttpResponse('Only the Restaurant keeper can manage the Orders !')


@login_required
def deletemeal(request, id):  
    if request.user.is_superuser:
        meal = Meal.objects.get(id=id)
        meal.delete()
        return redirect('order:meallist')
    else:
        return HttpResponse('Only the Restaurant keeper can manage the Meals !')


@login_required
def deletedesk(request, id):  
    if request.user.is_superuser:
        desk = Desk.objects.get(id=id)
        desk.delete()
        return redirect('order:desklist')
    else:
        return HttpResponse('Only the Restaurant keeper can manage the Desks !')
