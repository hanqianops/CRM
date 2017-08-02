# coding: utf-8
__author__ = "HanQian"
from django.conf.urls import url, include
from repository import views
urlpatterns = [
    url(r'^(\w+)/(\w+)/$', views.model_detail, name="model_detail"),
    url(r'^menu/$', views.menu, name="menu"),
    url(r'^test/$', views.test, name="test"),
    url(r'^index2/$', views.index2, name="index2"),
    url(r'^$', views.index, name="index"),
]
