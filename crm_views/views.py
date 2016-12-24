from django.shortcuts import render, redirect
from crm_models.models import *
from forms import *


# Create your views here.

def dashboard(request):
    params = {
        'location': 'main'
    }
    return render(request, 'view/dashboard.html', params)


def order_list(request):
    orders = Orders.objects.all()
    params = {
        'location': 'orders',
        'order_list': orders
    }

    return render(request, 'view/orders.html', params)


def new_order(request):
    form = CreateOrderForm
    if request.method is 'POST':
        return redirect('index')
    elif request.method is 'GET':
        params = {
            'order_form': CreateOrderForm
        }
        return render(request, 'view/forms/add_new_order.html', params)