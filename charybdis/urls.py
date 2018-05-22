"""Charybdis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from core import views as core_views

urlpatterns = [
    url('^login/$', auth_views.LoginView.as_view(), name='login'),
    url('^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url('^change-password/$', auth_views.PasswordChangeView.as_view(), name='change_password'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^search/', include('search.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^payment/', include('payment.urls')),
    url(r'^pricing/$', core_views.pricing, name='pricing'),
    url(r'^$', core_views.home, name='home'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
