# -*- coding: utf-8 -*-
from django.conf.urls import url

from dictionary import views


app_name = 'dictionary'
urlpatterns = [
    # ex: /
    url(r'^$', views.search, name='index'),
    # ex: search/
    url(r'^search/$', views.search, name="search"),
]
