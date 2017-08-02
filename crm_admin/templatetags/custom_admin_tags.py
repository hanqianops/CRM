# coding: utf-8
__author__ = "HanQian"
import re
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()  # register变量名是固定点


@register.simple_tag
def build_table_head(request, admin_class, ):
    """
    组合表头
    1、 获取本次的请求参数
    2、循环展示的列
    3、判断是否有排序的请求参数，如果有就处理排序字段 'field' or '-field'
    :param request: 请求参数
    :param admin_class:  其中封装了自定义的属性与需要的model对象
    :return:  HTML格式的表头信息
    """
    order_url = '?'
    for k, v in request.items():
        if v and k != "order":
            order_url += "%s=%s&" % (k, v)
    head_tr = "<th><input type='checkbox' onclick='SelectAllCancle(this);'></th>"
    if admin_class.list_display:
        for model_field in admin_class.list_display:
            field_obj = admin_class.model._meta.get_field(model_field)  # 获取model的字段的对象

            temp_order_url = order_url
            field_order = model_field
            icons = ""
            if request.get('order'):
                if request.get('order') == model_field:  # 不写这个会造成只对第一次点击的字段排序
                    if not request.get('order').startswith('-'):  # 升序或者降序
                        field_order = "-" + request.get('order')
                        icons = "<i class='fa fa-chevron-up' aria-hidden='true'></i>"
            temp_order_url += 'order=%s' % field_order
            head_tr += "<th> <a href='%s'>%s %s</i></a></th>" % (temp_order_url, field_obj.verbose_name, icons)
    else:
        head_tr += "<th> %s </th>" % ("无权限")
    head_tr += "<th>操作</th>"
    return mark_safe(head_tr)


@register.simple_tag
def build_filter_ele(filter_column, admin_class, filter_conditions):
    """
    1.拿到要过滤字段的对象field_obj
    2. 调用field_obj.get_choices()
    3. 生成select元素
    4.循环choices列表，生成option元素
    :param filter_column:
    :param model_class:
    :return:
    """
    field_obj = admin_class.model._meta.get_field(filter_column)
    select_ele = "<select class='form-control input-sm' onchange='Filter()' style='width: 150px; margin-right: 20px'  name=%s>" % filter_column
    filter_option = filter_conditions.get(filter_column)  # 1.None 代表没有对这个字段过滤，2.有值，选中的具体的option的val
    print('filter option', filter_option)

    if filter_option:  # 代表此字段过滤了
        for choice in field_obj.get_choices():
            if filter_option == str(choice[0]):
                selected = 'selected'
            else:
                selected = ''
            option_ele = "<option value=%s  %s>%s</option>" % (choice[0], selected, choice[1])
            select_ele += option_ele
            print(select_ele)
    else:
        for choice in field_obj.get_choices():
            if "---" in choice[1]:
                choice = ("", "请选择")
            option_ele = "<option value=%s >%s</option>" % (choice[0], choice[1])
            select_ele += option_ele

    select_ele += "</select>"
    return mark_safe(select_ele)


def edit_select(field_obj,column_val):
    select_ele = "<select class='form-control input-sm' style='margin: 1px'>"
    for choice in field_obj.get_choices():

        if choice[1] == column_val:
            print("选中")
            print('编辑', column_val, choice[1])
            option_ele = "<option value=%s name=%s selected >%s</option>" % (choice[0], choice[1], choice[1])
        else:
            print(choice[1],column_val,"buxiangd")
            option_ele = "<option value=%s name=%s >%s</option>" % (choice[0], choice[1], choice[1])
            select_ele += option_ele


    select_ele += "</select>"
    return select_ele


@register.simple_tag
def build_table_row(row, admin_class, ):
    """
    1.循环自定义的list_display , 取出每个字段的值
    2. 判断是否是第一个字段， 如果是，加a标签
    :param row:  一行数据
    :param admin_class: 自定义的属性
    :return:  <tr><td>xx</td>...</tr>
    """
    table_col = """ <td><input type='checkbox'name='checkbox' ></td> """
    for index, column_name in enumerate(admin_class.list_display):  # 循环一次就是一行数据
        # 取出 choices 字段的值，((0, '已报名'), (1, '已退费'), (2, '未报名'))
        # print("------",column_name)
        field_obj = row._meta.get_field(column_name)
        if field_obj.choices:
            column_val = eval("row.get_" + column_name + "_display()")  # 未报名、已退费、已报名
        else:
            column_val = getattr(row, column_name)

        if field_obj.get_internal_type() in ("SmallIntegerField", "ForeignKey"):  # 编辑状态下是否需要下拉菜单
            print("可编辑字段", column_name, type(field_obj.get_choices()))
            if column_name in getattr(admin_class, 'list_edit', ''):  # 是否可批量编辑
                table_col += "<td edit='true' >{column_val}</td><td class='hide'>{select}</td>".format(
                    column_val=column_val, select=edit_select(field_obj,column_val))
            else:
                table_col += "<td edit='false'>{column_val}</td>".format(column_val=column_val)

        else:
            if column_name in getattr(admin_class, 'list_edit', ''):  # 是否可批量编辑
                table_col += "<td edit='true' >{column_val}</td><td class='hide'><input type='text' value={column_val}></td>".format(
                    column_val=column_val)
            else:
                table_col += "<td edit='false'>{column_val}</td>".format(column_val=column_val)

    table_col += """
        <td>
        <a href='{id}/edit/'> 编辑 </a> |
        <a href='{id}/delete/'> 删除 </a> |
        <a href='{id}/detail/'> 查看详情 </a>
        </td>
        """.format(id=row.id)
    table_row = ''.join(["<tr>", table_col, "</tr>"])
    return mark_safe(table_row)


@register.assignment_tag
def title(admin_class):
    """可识别的表名"""
    if hasattr(admin_class, "name"):
        result = admin_class.name
    else:
        result = admin_class.model._meta.model_name
    return result


@register.assignment_tag
def menu(site):
    from django.urls import reverse
    for app_label, model_list in site.registered_admins.items():
        menu_str = """ <div class="collapse navbar-collapse navbar-ex1-collapse">

        <ul class="nav navbar-nav side-nav">
        <li class="active">
            <a href="#"><i class="fa fa-fw fa-dashboard"></i> %s</a>
        </li>
        """ % app_label
        for model_name, admin_class in model_list.items():
            url = reverse('crm_admin:obj_list', kwargs={"app_name": app_label, "model_name": model_name})

            menu_str += """<li style="padding-top: 0px;margin-left: 25px">
                <a href="%s"> %s </a>
            </li>""" % (url,admin_class.model._meta.verbose_name)


    return mark_safe(menu_str)
