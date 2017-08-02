# coding: utf-8
__author__ = "HanQian"
from django.conf.urls import url, include
from crm_admin import views
urlpatterns = [
    url(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/$', views.obj_list, name="obj_list"),
    url(r'^(\w+)/(\w+)/add/$', views.obj_add, name="obj_add"),
    url(r'^(\w+)/(\w+)/(\d+)/edit/$', views.obj_edit, name="obj_edit"),
    # url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.obj_delete, name="obj_delete"),
    url(r'^(\w+)/(\w+)/(\d+)/detail/$', views.obj_detail, name="obj_detail"),

    url(r'^test/$', views.test, name="test"),

    url(r'^$', views.index, name="index"),
]
