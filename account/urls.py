#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    # path(r'^$', views.index, name='account'),
    url(r'^$', views.AccountView.as_view(), name='account'),
]
