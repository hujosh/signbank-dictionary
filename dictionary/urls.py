# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from dictionary import views, adminviews


app_name = 'dictionary'
urlpatterns = [
    # ex: /
    url(r'^$', views.search, name='index'),
    # ex: search/
    url(r'^search/$', views.search, name="search"),
    # ex: words/jet-1
    url(r'^words/(?P<keyword>.+)-(?P<n>\d+)/$',
            views.word, name='word'),
    # ex: gloss/1        
    url(r'^gloss/(?P<idgloss>.+)/$', views.gloss,
         name='gloss'),
    # ex: gloss/4     
    url(r'^gloss/(?P<pk>\d+)/$', 
        permission_required('dictionary.search_gloss')(adminviews.GlossDetailView.as_view()), 
       name='admin_gloss_view'),
]
