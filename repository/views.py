import json

from django.shortcuts import render, HttpResponse

from crm import app_config
from crm.custom_admin import site
from repository import models
from django.db.models import Q
from utils.page import PageInfo


def menu(request):
    """生成左菜单"""
    f = models.Menu.objects.all()
    config = []
    for i in f:
        temp = {}
        temp['id'] = i.url
        temp['menu'] = []

        sub_dic = {}
        sub_dic['text'] = i.name
        sub_dic['items'] = []
        for sub in i.submenu_set.all():
            d = {}
            d['id'] = sub.id
            d['text'] = sub.name
            if not sub.url.endswith('/'):
                sub.url = sub.url+'/'
            d['href'] = sub.url
            sub_dic['items'].append(d)
        temp['menu'].append(sub_dic)
        config.append(temp)
    print(config)
    return HttpResponse(json.dumps(config))

def test(request):
    return  render(request, "customer/a.html")

def index(request):
    """首页"""
    return render(request, "repository/index.html",{'site':site})

def index2(request):
    """首页"""
    return render(request, "repository/index2.html",{'site':site})

def get_filter_objs(request,admin_class):
    """返回filter的结果queryset"""
    filter_condtions = {}
    page_url = {}
    q_obj = Q()
    q_obj.connector = "OR"

    for k,v in request.GET.items():
        if k == 'page': continue
        if k == "search" and v:
            for search_field in admin_class.search_fields:
                q_obj.children.append(("%s__contains"%search_field,v))
                page_url[k] = v
            continue
        if v:
            filter_condtions[k] = v
        page_url[k] = v

    queryset = admin_class.model.objects.filter(**filter_condtions,)
    queryset = queryset.filter(q_obj)
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



def model_detail(request, app_name, model_name):
    if app_name in site.registered_admins:                  # 是否有 repository应用
        if model_name in site.registered_admins[app_name]:  # 是否有 course models
            admin_class = site.registered_admins[app_name][model_name]  # 获取 具体models的实例
            querysets,filter_condtions,page_filter = get_filter_objs(request,admin_class)
            current_page = request.GET.get("page")
            print("page_filter=======",page_filter)
            page_info = PageInfo(current_page, 5, len(querysets),request.path,filter=page_filter)
            querysets = querysets[page_info.start:page_info.end]
            return render(request, "repository/obj_list.html", locals())

from django.views.generic import View,ListView

