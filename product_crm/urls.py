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
# from django.contrib.auth import logout

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from crm_views.views import *

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_user, name='login_user'),
    url(r'^logout/$', logout_user, name='logout_user'),
    url(r'^user/current/profile$', current_user_profile, name='user_profile'),
    url(r'^$', dashboard, name='index'),
    url(r'^orders/list$', order_list, name='order_list'),
    url(r'^orders/new$', new_order, name='order_new'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()