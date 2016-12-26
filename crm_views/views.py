# coding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from forms import *
from crm_models.models import *


# Create your views here.

@csrf_exempt
def login_user(request):
    form = LoginForm(request.POST)
    params = {
        'login_form': form
    }
    logout(request)
    username = password = ''
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    params['message'] = 'Не правильный логин или пароль'
            else:
                params['message'] = 'Неправильный логин или пароль'
        else:
            params['message'] = 'Неправильно заполнена форма'

    return render_to_response('view/user/login.html', params)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_user'))


@login_required
def dashboard(request):
    params = {
        'location': 'dashboard'
    }
    return render(request, 'view/dashboard.html', params)


@login_required
def order_list(request):
    paginator = Paginator(Orders.objects.all(), 20)
    orders = paginator.page(request.GET.get('page', 1))
    params = {
        'location': 'orders',
        'order_list': orders
    }

    return render(request, 'view/orders.html', params)


@csrf_exempt
@login_required
def new_order(request):
    form = CreateOrderForm(request.POST)
    params = {
        'order_form': form,
        'request': request
    }
    if request.POST:
        if form.is_valid():
            try:
                nds = 1.5
                order = form.instance
                order.final_price = float(order.price) * nds
                order.save()

                return HttpResponseRedirect(reverse('order_list'))
            except:
                params.update(dict(message='Ошибка при заполнении'))
                return render(request, 'view/forms/add_new_order.html', params)
        print 'form error:' + form.errors

    return render(request, 'view/forms/add_new_order.html', params)


@login_required
def remove_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    order.delete()
    return HttpResponseRedirect(reverse('order_list'))


@login_required
def view_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    params = {
        'order': order
    }
    return render(request, 'view/showcase/order.html', params)


@login_required
def current_user_profile(request):
    params = {
        'location': 'profile'
    }
    return render(request, 'view/user/profile.html', params)
