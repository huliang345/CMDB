#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^asset/', views.AssetView.as_view()),
    re_path(r'^asset-json.html$', views.AssetJsonView.as_view()),
    re_path(r'^business-unit.html$', views.BusinessUnitView.as_view()),
    re_path(r'^business-unit-json.html$', views.BusinessUnitJsonView.as_view()),
]


