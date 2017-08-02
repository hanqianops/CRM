# coding: utf-8
__author__ = "HanQian"

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()   # register变量名是固定点

@register.simple_tag
def build_filter_ele(filter_column,admin_class,filter_conditions):
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
    select_ele = "<select class='form-control input-sm' onchange='Filter()' style='width: 150px; margin-right: 20px'  name=%s>"% filter_column
    filter_option = filter_conditions.get(filter_column) #1.None 代表没有对这个字段过滤，2.有值，选中的具体的option的val
    print('filter option',filter_option)

    if filter_option:       #代表此字段过滤了
        for choice in field_obj.get_choices():
            if filter_option == str(choice[0]):
                selected = 'selected'
            else:
                selected = ''
            option_ele = "<option value=%s  %s>%s</option>" % (choice[0],selected,choice[1])
            select_ele += option_ele
            print(select_ele)
    else:
        for choice in field_obj.get_choices():
            if "---" in choice[1]:
                choice = ("","请选择")
            option_ele = "<option value=%s >%s</option>" % (choice[0], choice[1])
            select_ele += option_ele

    select_ele += "</select>"
    print("=====",select_ele)
    return mark_safe(select_ele)


@register.simple_tag
def build_table_row(row,admin_class):
    """
    1.循环自定义的list_display , 取出每个字段的值
    2. 判断是否是第一个字段， 如果是，加a标签
    :param row:  一行数据
    :param admin_class: 自定义的属性
    :return:  <tr><td>xx</td>...</tr>
    """
    table_row = "<tr>"
    for index,(column_name,_) in enumerate(admin_class.list_display):
        # 取出 choices 字段的值，((0, '已报名'), (1, '已退费'), (2, '未报名'))
        field_obj = row._meta.get_field(column_name)
        if field_obj.choices:
            print(column_name,"]]]]]]]]]]]]]]]]")
            column_val = eval("row.get_"+column_name+"_display()")  # 未报名、已退费、已报名
        else:
            column_val = getattr(row,column_name)

        if index == 0:
            table_col = "<td><a href='#'>{column_val}</a></td>".format(column_val=column_val)
        else:
            table_col = "<td>{column_val}</td>".format(column_val=column_val)

        table_row += table_col  # 每一列的数据

    table_row += "</tr>"   # 一行的数据
    return mark_safe(table_row)


@register.assignment_tag
def title(admin_class):
    """可识别的模型名字"""
    if hasattr(admin_class,"name"):
        result = admin_class.name
    else:
        result = admin_class.model._meta.model_name
    return result
