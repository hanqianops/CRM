from django.contrib import admin
from repository import models
# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    """创建新用户的表单。包括所有必需的字段，加上重复的密码"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.Account
        fields = ('email', 'name','is_active','is_admin')

    def clean_password2(self):
        # 检查密码是否匹配
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """更新用户的表单。包含用户上的所有字段，但用admin的密码哈希显示字段替换密码字段"""

    password = ReadOnlyPasswordHashField()
    class Meta:
        model = models.Account
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('test', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','customer')}),
        ('Permissions', {'fields': ('is_admin','role')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(models.Account, AccountAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','qq','source',"referral_from",'consultant','status')
    list_filter = ('source','status','consultant')
    search_fields = ['qq','source__name']

admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.ClassList)
admin.site.register(models.Contract)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Tag)
admin.site.register(models.Role)
admin.site.register(models.Enrollment)
admin.site.register(models.SubMenu)
admin.site.register(models.Menu)
admin.site.register(models.Branch)
admin.site.register(models.Source)
admin.site.register(models.Course)
admin.site.register(models.PaymentRecord)

