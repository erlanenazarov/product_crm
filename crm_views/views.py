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
from django.contrib.auth.models import *


# Create your views here.

def generate_view_params(request):
    notifications = Notification.objects.filter(is_read=False)
    user_notification = list()
    for notification in notifications:
        print notification.user
        if request.user in notification.user.all():
            user_notification.append(notification)

    params = {
        'notifications_count': len(user_notification),
        'notifications': user_notification
    }
    return params


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
        'location': 'dashboard',
        'order_count': Orders.objects.all().count(),
        'user_count': User.objects.all().count(),
        'clients_count': Client.objects.all().count(),
    }
    params.update(generate_view_params(request))
    return render(request, 'view/dashboard.html', params)


@login_required
def order_list(request):
    paginator = Paginator(Orders.objects.all(), 20)
    orders = paginator.page(request.GET.get('page', 1))
    params = {
        'location': 'orders',
        'order_list': orders
    }
    params.update(generate_view_params(request))

    return render(request, 'view/orders.html', params)


@csrf_exempt
@login_required
def new_order(request):
    form = OrderForm(request.POST)
    params = {
        'order_form': form,
        'request': request,
        'location': 'orders'
    }
    if request.POST:
        if form.is_valid():
            try:
                nds = 1.5
                order = form.instance
                order.final_price = float(order.price) * nds
                order.save()
                notification = Notification()
                notification.message = u'You have a new order!'
                notification.url = reverse('order_view', kwargs={'order_id': order.id})
                notification.save()
                notification.user.add(request.user)
                notification.save()

                return HttpResponseRedirect(reverse('order_list'))
            except Exception, e:
                params.update(dict(message=e))
                return render(request, 'view/forms/add_new_order.html', params)

        print 'form error:' + form.errors

    params.update(generate_view_params(request))

    return render(request, 'view/forms/add_new_order.html', params)


@login_required
def remove_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    notifications = Notification.objects.filter()
    order_comments = OrderComment.objects.filter(order_id=order)
    order_comments.delete()
    order.delete()
    return HttpResponseRedirect(reverse('order_list'))


@login_required
def view_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    comments = OrderComment.objects.filter(order_id=order)
    comments_form = CommentForm
    params = {
        'order': order,
        'comments': comments,
        'comments_form': comments_form,
        'location': 'orders'
    }
    params.update(generate_view_params(request))
    return render(request, 'view/showcase/order.html', params)


@csrf_exempt
@login_required
def edit_order(request, order_id):
    order = Orders.objects.get(id=order_id)
    if request.POST:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            nds = 1.5
            instance = form.instance
            instance.final_price = float(instance.price) * nds
            instance.save()
            return HttpResponseRedirect(reverse('order_list'))
    else:
        form = OrderForm(instance=order)
    params = {
        'order_form': form,
        'order': order,
        'location': 'orders'
    }
    params.update(generate_view_params(request))

    return render(request, 'view/forms/edit_order.html', params)


@csrf_exempt
@login_required
def edit_dashboard_order(request, order_id):
    if request.POST:
        order = Orders.objects.get(id=order_id)
        order.title = request.POST.get('title')
        order.status = request.POST.get('status')
        order.save()
        order_template = render_to_response('view/misc/order_dashboard_row.html', {'item': order})
        return order_template
    else:
        return HttpResponse('')


@csrf_exempt
def list_comments(request):
    if request.POST.get('order_id'):
        comments = OrderComment.objects.filter(order_id_id=request.POST.get('order_id'))
    else:
        comments = OrderComment.objects.all()

    params = {
        'comments': comments
    }
    return render_to_response('view/misc/comments.html', params)


@csrf_exempt
def add_comment(request):
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                comment = comment_form.instance
                comment.save()
                return JsonResponse(dict(success=True))
            except:
                return JsonResponse(dict(success=False))

    return JsonResponse(dict(success=False))


@login_required
def current_user_profile(request):
    params = {
        'location': 'profile'
    }
    params.update(generate_view_params(request))
    return render(request, 'view/user/profile.html', params)


@login_required
def list_clients(request):
    paginator = Paginator(Client.objects.all(), 20)
    clients = paginator.page(request.GET.get('page', 1))
    params = {
        'clients': clients,
        'location': 'clients'
    }
    params.update(generate_view_params(request))
    return render(request, 'view/clients.html', params)


@csrf_exempt
@login_required
def new_client(request):
    client_form = ClientForm(request.POST)
    params = {
        'client_form': client_form,
        'location': 'clients'
    }

    if request.POST:
        if client_form.is_valid():
            client = client_form.instance
            client.save()
            return HttpResponseRedirect(reverse('client_list'))

    params.update(generate_view_params(request))
    return render(request, 'view/forms/add_new_client.html', params)


@login_required
def remove_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
    return HttpResponseRedirect(reverse('client_list'))


@csrf_exempt
@login_required
def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.POST:
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            instance = form.instance
            instance.save()
            return HttpResponseRedirect(reverse('client_list'))
    else:
        form = ClientForm(instance=client)
    params = {
        'client_form': form,
        'client': client,
        'location': 'clients'
    }
    params.update(generate_view_params(request))

    return render(request, 'view/forms/edit_client.html', params)


@login_required
def view_client(request, client_id):
    client = Client.objects.get(id=client_id)
    params = {
        'client': client,
        'location': 'clients'
    }
    params.update(generate_view_params(request))
    return render(request, 'view/showcase/client.html', params)


@csrf_exempt
@login_required
def edit_dashboard_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.name = request.POST.get('name')
    client.email = request.POST.get('email')
    client.phone_number = request.POST.get('phone')
    client.address = request.POST.get('address')
    client.save()
    return JsonResponse(dict(success=True))
