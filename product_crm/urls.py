"""product_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import logout

from django.contrib.admin import site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from crm_views.views import *

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', site.urls),
    url(r'^login/$', login_user, name='login_user'),
    url(r'^logout/$', logout_user, name='logout_user'),
    url(r'^user/current/profile$', current_user_profile, name='user_profile'),
    url(r'^$', dashboard, name='index'),
    url(r'^orders/list$', order_list, name='order_list'),
    url(r'^orders/new$', new_order, name='order_new'),
    url(r'^orders/remove/(?P<order_id>[0-9]+)$', remove_order, name='order_remove'),
    url(r'^orders/view/(?P<order_id>[0-9]+)$', view_order, name='order_view'),
    url(r'^orders/edit/(?P<order_id>[0-9]+)$', edit_order, name='order_edit'),
    url(r'^orders/edit/dashboard/(?P<order_id>[0-9]+)$', edit_dashboard_order, name='order_edit_dashboard'),
    url(r'^comments/add$', add_comment, name='add_comment'),
    url(r'^comments/all$', list_comments, name='all_comments'),
    url(r'^users/list$', list_clients, name='client_list'),
    url(r'^users/new$', new_client, name='client_new'),
    url(r'^users/remove/(?P<client_id>[0-9]+)$', remove_client, name='client_remove'),
    url(r'^users/edit/(?P<client_id>[0-9]+)$', edit_client, name='client_edit'),
    url(r'^users/view/(?P<client_id>[0-9]+)$', view_client, name='client_view'),
    url(r'^users/edit/dashboard/(?P<client_id>[0-9]+)$', edit_dashboard_client, name='client_edit_dashboard'),
    url(r'^managers/list$', list_users, name='user_list'),
    url(r'^managers/add$', add_user, name='user_add'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
