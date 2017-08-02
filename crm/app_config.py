# coding: utf-8
__author__ = "HanQian"

from crm import settings

for app_name  in settings.INSTALLED_APPS:
    try:
        __import__( "%s.%s" %(app_name,"custom_admin"))
    except ImportError:
        pass