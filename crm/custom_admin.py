# coding: utf-8
__author__ = "HanQian"

class BaseAdmin(object):

    list_display = ()
    list_filter = ()
    search_fields = ()
    list_per_page = 5

class AdminSite(object):
    def __init__(self):
        self.registered_admins = {}

    def register(self, model_or_iterable, admin_class=BaseAdmin, **options):
        """
        负责把每个App下的表注册self.registered_admins集合里
        """
        # admin_class.model.objects.filter() == models.xxx.objects.filter()
        admin_class.model = model_or_iterable

        app_label = model_or_iterable._meta.app_label
        if app_label not in self.registered_admins:
            self.registered_admins[app_label] =  {}
        self.registered_admins[app_label][model_or_iterable._meta.model_name] = admin_class


site = AdminSite()