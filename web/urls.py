# coding: utf-8
__author__ = "HanQian"

from django.conf.urls import url
from web import views
urlpatterns = [
    url(r'^$',views.index),
    # url(r'^crm/', include('web.urls',namespace="web")),
]