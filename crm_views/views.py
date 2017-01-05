# coding=utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.shortcuts import render_to_response
from django.contrib.auth import *
from forms import *
from crm_models.models import *
from django.contrib.auth.models import *
from datetime import date, datetime


# Create your views here.

def generate_view_params(request):
    params = {

    }
    params.update(get_user_notifications(request))
    return params


def get_user_notifications(request):
    notifications = Notification.objects.filter(user__in=[request.user]).order_by('-id')
    user_notification = list()
    unread_notifications = 0
    for notification in notifications:
        if notification.is_read is False:
            unread_notifications += 1
        user_notification.append(notification)

    params = {
        'notifications_count': unread_notifications,
        'notifications': user_notification
    }
    return params


@csrf_exempt
def list_notifications(request):
    return JsonResponse(get_user_notifications(request))


def add_new_notification(message, url, user, order):
    try:
        notification = Notification()
        notification.message = message
        notification.url = url
        notification.order = order
        notification.is_read = False
        notification.save()
        if user is not None:
            for u in user:
                notification.user.add(u)
        notification.save()
        return True
    except Exception, e:
        print e
        return False


@login_required
def view_notification(request, not_id):
    notification = Notification.objects.get(id=not_id)
    notification.is_read = True
    notification.save()
    return HttpResponseRedirect(notification.url)


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
                managers = list(form.cleaned_data['manager'])
                for manager in managers:
                    order.manager.add(manager)
                tags = list(form.cleaned_data['tags'])
                for tag in tags:
                    order.tags.add(tag)
                order.save()
                add_new_notification(
                    u'Вы были добавлены в новый заказ!',
                    reverse('order_view', kwargs={'order_id': order.id}),
                    managers,
                    order
                )

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
                order = comment_form.cleaned_data['order_id']
                add_new_notification(
                    u'Добавлен новый комментарий к заказу!',
                    reverse('order_view', kwargs={'order_id': comment.order_id.id}),
                    order.manager.all(),
                    order
                )
                return JsonResponse(dict(success=True))
            except Exception, e:
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


@login_required
def list_users(request):
    paginator = Paginator(User.objects.all(), 20)
    users = paginator.page(request.GET.get('page', 1))

    params = {
        'location': 'users',
        'users': users
    }
    params.update(generate_view_params(request))
    return render(request, 'view/users.html', params)


@csrf_exempt
@login_required
def add_user(request):
    user_form = UserForm(request.POST)
    params = {
        'location': 'users',
        'user_form': user_form,
        'current_date': datetime.today()
    }
    if request.POST:
        if user_form.is_valid():
            user = user_form.instance
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('user_list'))
        else:
            params.update(dict(message='Ошибка', errors=user_form.errors))
    params.update(generate_view_params(request))
    return render(request, 'view/forms/add_new_user.html', params)


@csrf_exempt
@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.POST:
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            instance = user_form.instance
            instance.save()
            return HttpResponseRedirect(reverse('user_list'))
    else:
        user_form = UserForm(instance=user)

    params = {
        'user_form': user_form,
        'location': 'users',
        'user': user
    }
    params.update(generate_view_params(request))
    return render(request, 'view/forms/edit_user.html', params)


@login_required
def remove_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('user_list'))


@csrf_exempt
@login_required
def edit_dashboard_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()
    return JsonResponse(dict(success=True))
