#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r'^asset/$', views.asset),  # 传参要么是变量要么是字符串数字等数据类型
]
