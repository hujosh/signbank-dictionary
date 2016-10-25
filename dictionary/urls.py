# -*- coding: utf-8 -*-
from django.conf.urls import url

from dictionary import views


app_name = 'dictionary'
urlpatterns = [
    # ex: /
    url(r'^$', views.search, name='index'),
    # ex: search/
    url(r'^search/$', views.search, name="search"),
    # ex: words/jet-1
    url(r'^words/(?P<keyword>.+)-(?P<n>\d+)/$',
            views.word, name='word'),
]
