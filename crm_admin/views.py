import json

from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, HttpResponse,redirect

from crm_admin import config
from crm_admin import forms
from crm_admin.base import site
from repository import models
from utils.page import PageInfo

print("admin_class",site.registered_admins)

def test(request):
    from django.forms.models import modelformset_factory
    from crm_admin import config
    from crm_admin.base import site
    admin_class = site.registered_admins['repository']['customer']
    formset = modelformset_factory(admin_class.model, fields=('name','source','id'), )
    formset = formset(queryset=models.Customer.objects.filter(pk=1011))
    # return  render(request, "crm_admin/a.html",locals())
    print("----------",type(formset.as_table()))
    return  HttpResponse(formset.as_table())

def index(request):
    """首页"""
    return render(request, "crm_admin/index.html")

def get_filter_objs(request,admin_class):
    """返回filter的结果queryset"""
    filter_condtions = {}
    page_url = {}
    q_obj = Q()
    q_obj.connector = "OR"

    for k,v in request.GET.items():
        if k in ('page','page_num'):
            continue
        if k == 'order':
            page_url[k] = v
            continue
        page_url[k] = v   # 记录get参数，用于组合分页url： ?page=6&search=w&source=&status=&referral_from=1

        if k == "search" and v:
            for search_field in admin_class.search_fields:
                q_obj.children.append(("%s__contains"%search_field,v))
            continue
        if v:
            filter_condtions[k] = v

    queryset = admin_class.model.objects.filter(**filter_condtions,).filter(q_obj)
    return queryset,filter_condtions,page_url

class ModelHandle(object):
    def __init__(self, request, admin_class):
        self.request = request
        self.admin_class = admin_class

    def filter(self):
        """<select></select>组合过滤"""
        filter_condtions = {}
        for k, v in self.request.GET.items():
            if v and k not in ["p", "q", ]:
                filter_condtions[k] = v
        print("过滤的字段",filter_condtions)
        queryset = self.admin_class.model.objects.filter(**filter_condtions)
        queryset = queryset.filter(self.search())
        print("过滤处理后的对象",queryset,)
        return queryset, filter_condtions

    def search(self):
        """
        返回搜索后的对象列表
        """
        q_obj = Q()
        q_obj.connector = "OR"
        search_text = self.request.GET.get("q",'')
        for search_field in self.admin_class.search_fields:
            q_obj.children.append(("%s__contains" % search_field, search_text))
        print("Q 查询",q_obj)
        return q_obj

    def page(self):
        """分页"""
        obj_list,filter_condtions = self.filter()
        current_page = self.request.GET.get("p")
        base_url = self.request.path_info
        print("====>>>>", base_url)
        page_info = PageInfo(current_page, 5, len(obj_list), base_url, filter=filter_condtions)
        obj_list = obj_list[page_info.start:page_info.end]
        # return obj_list

from django.views.generic import ListView


# class ObjList(ListView):
#     def dispatch(self, request, *args, **kwargs):
#         if request.GET.get("page_num"):
#             request.session['page_num'] = int(request.GET.get("page_num"))
#         elif request.session.get("page_num"):
#             pass
#         else:
#             request.session['page_num'] = 1
#         if app_name in site.registered_admins:  # 是否有 repository应用
#             if model_name in site.registered_admins[app_name]:  # 是否有 course models
#                 admin_class = site.registered_admins[app_name][model_name]  # 获取 具体models的实例
#
#     def get_queryset(self,request):
#         if app_name in site.registered_admins:  # 是否有 repository应用
#             if model_name in site.registered_admins[app_name]:  # 是否有 course models
#                 admin_class = site.registered_admins[app_name][model_name]  # 获取 具体models的实例
#                 querysets, filter_condtions, page_filter = get_filter_objs(request, admin_class)
#
#                 # 字段排序
#                 order = request.GET.get("order")
#                 if order:
#                     querysets = querysets.order_by(order)
#                 current_page = request.GET.get("page")
#
#                 print("page_filter=======", page_filter)
#                 page_info = PageInfo(current_page,
#                                      request.session['page_num'],
#                                      len(querysets),
#                                      request.path,
#                                      filter=page_filter)
#                 querysets = querysets[page_info.start:page_info.end]




def obj_list(request, app_name, model_name):
    if request.GET.get("page_num"):
        request.session['page_num'] = int(request.GET.get("page_num"))
    elif request.session.get("page_num"):
        pass
    else:
        request.session['page_num'] = 1

    if app_name in site.registered_admins:                  # 是否有 repository应用
        if model_name in site.registered_admins[app_name]:  # 是否有 course models
            admin_class = site.registered_admins[app_name][model_name]  # 获取 具体models的实例
            querysets,filter_condtions,page_filter = get_filter_objs(request,admin_class)

            # 字段排序
            order = request.GET.get("order")
            if order:
                querysets = querysets.order_by(order)
            current_page = request.GET.get("page")

            print("page_filter=======",page_filter)
            page_info = PageInfo(current_page,
                                 request.session['page_num'],
                                 len(querysets),
                                 request.path,
                                 filter=page_filter)
            querysets = querysets[page_info.start:page_info.end]

            return render(request, "crm_admin/obj_list.html", locals())


def obj_add(request,app_name,model_name):
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]

            form = forms.create_modelform(admin_class.model)
            if request.method == "GET":
                form_obj = form()
            elif request.method == "POST":
                form_obj = form(data=request.POST)
                if form_obj.is_valid():
                    form_obj.save()

                    return redirect(request.path.rstrip("add/"))
    return render(request, 'crm_admin/obj_add.html', locals())

def obj_edit(request, app_name, model_name,obj_id):
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]
            object = admin_class.model.objects.get(id=obj_id)
            form = forms.create_modelform(admin_class.model)
        if request.method == "GET":
            form_obj = form(instance=object)
        else:
            form_obj = form(instance=object,data=request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(reverse('crm_admin:obj_list',kwargs={"app_name":app_name,"model_name":model_name}))
    return render(request, "crm_admin/obj_add.html", locals())


def obj_detail(request, app_name, model_name,obj_id):
    if app_name in site.registered_admins:
        if model_name in site.registered_admins[app_name]:
            admin_class = site.registered_admins[app_name][model_name]
            object = admin_class.model.objects.get(id=obj_id)
            form = forms.create_modelform(admin_class.model)
            form_obj = form(instance=object)

    return render(request, "crm_admin/obj_detail.html", locals())






















