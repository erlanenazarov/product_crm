# coding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
                    return HttpResponseRedirect('/')
                else:
                    params['message'] = 'Не правильный логин или пароль'
            else:
                params['message'] = 'Неправильный логин или пароль'
        else:
            params['message'] = 'Неправильно заполнена форма'

    return render_to_response('view/user/login.html', params)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login/')
def dashboard(request):
    params = {
        'location': 'dashboard'
    }
    return render(request, 'view/dashboard.html', params)


@login_required(login_url='/login/')
def order_list(request):
    paginator = Paginator(Orders.objects.all(), 20)
    orders = paginator.page(request.GET.get('page', 1))
    params = {
        'location': 'orders',
        'order_list': orders
    }

    return render(request, 'view/orders.html', params)


@csrf_exempt
@login_required(login_url='/login/')
def new_order(request):
    form = CreateOrderForm(request.POST)
    params = {
        'order_form': form
    }
    if request.POST:
        if form.is_valid():
            try:
                nds = 1.5
                order = Orders()
                order.title = form.cleaned_data['title']
                order.price = form.cleaned_data['price']
                order.final_price = float(order.price) * nds
                order.status = form.cleaned_data['status']
                order.order_number = form.cleaned_data['order_number']
                order.link_to_product = form.cleaned_data['link_to_product']
                order.site_which_from = form.cleaned_data['site_which_from']
                order.extra_field = form.cleaned_data['extra_field']
                order.tags = form.cleaned_data['tags']
                order.client = form.cleaned_data['client']
                order.manager = form.cleaned_data['manager']
                order.done = form.cleaned_data['done']
                order.save()

                return HttpResponseRedirect('/orders/list/')
            except:
                params.update(dict(message='Ошибка при заполнении'))
                return render(request, 'view/forms/add_new_order.html', params)

        print 'form is not valid!'

    return render(request, 'view/forms/add_new_order.html', params)


@login_required(login_url='/login/')
def current_user_profile(request):
    params = {
        'location': 'profile'
    }
    return render(request, 'view/user/profile.html', params)
