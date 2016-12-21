from django.shortcuts import render
from crm_models.models import *


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
