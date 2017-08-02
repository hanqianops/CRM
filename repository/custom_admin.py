# coding: utf-8
__author__ = "HanQian"
print("导入 自定义的admin配置=====================================================")
from repository import models
from crm_admin.base import BaseAdmin, site
class CustomerAdmin(BaseAdmin):
    list_display = ('id', 'name', 'referral_from', 'source', 'status', 'phone')
    list_filter = (("referral_from","介绍人"),("source","顾客来源"),("status","状态"))
    search_fields = ("name","source__name")
    list_edit = ('referral_from','source','status','phone')

class PaymentRecordAdmin(BaseAdmin):
    list_display = ('customer', 'class_list', 'payment_method', 'account')

class CourseAdmin(BaseAdmin):
    list_display = ('name', 'period', 'price', 'outline')

class ClassListAdmin(BaseAdmin):
    list_display = ('semester', 'course', 'branch')


class CourseRecordAdmin(BaseAdmin):
    list_display = ('name', 'class_list', 'day_num', 'day_num', 'teacher')


class StudyRecordAdmin(BaseAdmin):
    list_display = ('student', 'score', 'show_status', 'comment')
    list_edit = ('student', 'show_status')
    list_filter = (("score","成绩"), ("show_status","考勤"))
    name = "学习记录"


site.register(models.PaymentRecord,PaymentRecordAdmin)
site.register(models.StudyRecord,StudyRecordAdmin)
site.register(models.CourseRecord,CourseRecordAdmin)
site.register(models.Customer,CustomerAdmin)
site.register(models.Course,CourseAdmin)
site.register(models.ClassList, ClassListAdmin)
# site.register(models.Menu,MenuAdmin)
