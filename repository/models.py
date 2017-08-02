from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Source(models.Model):
    """客户来源"""
    name = models.CharField(verbose_name="来源",max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户来源"
        verbose_name_plural = "客户来源"

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    """顾客"""
    name = models.CharField("姓名",max_length=64, blank=True, null=True)
    qq = models.CharField("QQ",max_length=64,  blank=True, null=True)
    weixin = models.CharField("微信",max_length=64,  blank=True, null=True)
    phone = models.BigIntegerField("电话", blank=True, null=True)
    email = models.EmailField("邮件",blank=True, null=True)
    status_choices = ((0,'已报名'), (1, '已退费'), (2, '未报名'),)
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices,default=2)
    content = models.TextField("首次咨询内容/客户详情")

    source = models.ForeignKey(verbose_name="客户来源", to="Source")
    referral_from = models.ForeignKey(verbose_name="介绍人",to="Account", blank=True, null=True, related_name="my_referral")
    consult_courses = models.ManyToManyField(verbose_name="咨询的课程",to="Course")
    tags = models.ManyToManyField("Tag",blank=True)
    consultant = models.ForeignKey(verbose_name="接待人员",to="Account",related_name="my_consultant")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" %self.name
    class Meta:
        verbose_name = "客户信息表"
        verbose_name_plural = "客户信息表"

class PaymentRecord(models.Model):
    """缴费记录"""
    customer = models.ForeignKey(verbose_name="姓名",to="Customer")
    class_list = models.ForeignKey(verbose_name="班级",to="ClassList")
    payment_method_choices = ((0,'现金'), (1, '支付宝'), (2, '刷卡'))
    payment_method = models.SmallIntegerField(verbose_name="支付方式",choices=payment_method_choices)
    payment_type_choices = ((0,'报名费'), (1, '学费'), (2, '退费'),)
    payment_type = models.SmallIntegerField(verbose_name="支付类型",choices=payment_type_choices)
    amount = models.IntegerField()
    account = models.ForeignKey(verbose_name="收款人",to="Account")
    date = models.DateTimeField(verbose_name="时间",auto_now_add=True)

    class Meta:
        verbose_name = "缴费记录"
        verbose_name_plural = "缴费记录"

class CustomerFollowUp(models.Model):
    """记录顾客意向，跟进顾客"""
    customer = models.ForeignKey(verbose_name="客户姓名",to="Customer")
    content = models.TextField(verbose_name="咨询的内容")
    consultant = models.ForeignKey(verbose_name="课程顾问",to="Account")   # 接待人
    date = models.DateTimeField(verbose_name="时间",auto_now_add=True)
    status_choices = ((0,'绝不考虑'),
                      (1, '短期内不考虑'),
                      (2, '已在其它机构报名'),
                      (3, '2周内报名'),
                      (4, '已报名'),
                      (5, '已试听'),
                      )
    status = models.IntegerField(verbose_name="客户意向",choices=status_choices)

    class Meta:
        verbose_name = "客户意向表"
        verbose_name_plural = "客户意向表"

class Course(models.Model):
    """课程"""
    name = models.CharField(verbose_name="课程名",max_length=128,unique=True)
    period = models.IntegerField(verbose_name="学习周期(月)")
    price = models.IntegerField(verbose_name="价格")
    outline = models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"

class Branch(models.Model):
    """校区"""
    name = models.CharField(verbose_name="校区",max_length=64,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "校区"
        verbose_name_plural = "校区"

class ClassList(models.Model):
    """班级"""
    course = models.ForeignKey(verbose_name="课程", to="Course")
    branch = models.ForeignKey(verbose_name="校区", to="Branch")
    semester = models.IntegerField(verbose_name="学期")
    class_type_choices = ((0,'周末'),(1,'脱产'),(2,'网络'))
    class_type = models.SmallIntegerField(verbose_name="上课类型", choices=class_type_choices)
    max_student_num = models.IntegerField(verbose_name="人数", default=80)
    teachers = models.ManyToManyField(verbose_name="讲师", to="Account")
    contract = models.ForeignKey(verbose_name="入学合同", to="Contract")   # 合同
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期",blank=True,null=True)

    def __str__(self):
        return "%s(%s)" %(self.course,self.semester)

    class Meta:
        verbose_name = "班级列表"
        verbose_name_plural = "班级列表"
        # 联合唯一索引，两者的组合必须是唯一的
        unique_together = ('course','branch','semester','class_type')


class CourseRecord(models.Model):
    """上课记录"""
    class_list = models.ForeignKey(verbose_name="班级", to="ClassList")
    day_num = models.IntegerField(verbose_name="节次")
    name = models.CharField(verbose_name="学院姓名", max_length=128)
    teacher = models.ForeignKey(verbose_name="讲师", to="Account")
    has_homework = models.BooleanField(verbose_name="是否有项目", default=True)
    homework_title = models.CharField(verbose_name="项目",max_length=128,blank=True,null=True)
    homework_requirement = models.TextField(verbose_name="项目需求",blank=True,null=True)   # 作业要求
    date = models.DateTimeField(verbose_name="时间",auto_now_add=True)

    def __str__(self):
        return "%s(%s)-%s" %(self.class_list,self.day_num,self.name)
    class Meta:
        verbose_name = "上课记录"
        verbose_name_plural = "上课记录"
        unique_together = ('class_list','day_num')

class Enrollment(models.Model):
    """已报名课程"""
    account = models.ForeignKey("Account")
    class_list = models.ForeignKey("ClassList")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "已报名的课程"
        verbose_name_plural = "已报名的课程"

class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey(verbose_name="学员姓名",to="Account",related_name='aaa')
    course_record = models.ForeignKey(verbose_name="上课记录",to="CourseRecord")
    score_choices = ((100,'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (70,'B'),
                     (65,'C+'),
                     (60,'C'),
                     (40,'C-'),
                     (-50,'D'),
                     (0,'N/A'),
                     (-100,'COPY'),
                     )
    score = models.IntegerField(verbose_name="成绩", choices=score_choices, blank=True,null=True)
    show_status_choices = ((0,'正常签到'),(1,'迟到'),(2,'缺勤'),(3,'N/A'))
    show_status = models.SmallIntegerField(verbose_name="出勤情况",choices=show_status_choices)
    comment = models.TextField(verbose_name="批注",blank=True,null=True)
    date  = models.DateTimeField(verbose_name="时间",auto_now_add=True)

    def __str__(self):
        return str(self.student)

    class Meta:
        verbose_name = "学习记录"
        verbose_name_plural = "学习记录"
        # unique_together = ("student",'course_record')



class Contract(models.Model):
    """合同"""
    name = models.CharField(max_length=128,unique=True)
    content = models.TextField("合同内容")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "合同表"
        verbose_name_plural = "合同表"

class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64,unique=True)
    menus = models.ManyToManyField("Menu",blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"

class Menu(models.Model):
    """一级菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = ((0,'absolute'),(1,'relative'))
    url_type =  models.PositiveIntegerField(choices=url_type_choices,default=1)
    url = models.CharField(max_length=128)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("url",'url_type')

class SubMenu(models.Model):
    """二级菜单"""
    menu = models.ForeignKey("Menu")
    name = models.CharField(max_length=64)
    url_type_choices = ((0, 'absolute'), (1, 'relative'))
    url_type = models.PositiveIntegerField(choices=url_type_choices, default=1)
    url = models.CharField(max_length=128)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("url", 'url_type')

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """ 创建用户 """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """ 创建超级用户 """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    """自定义"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    role = models.ForeignKey("Role",blank=True,null=True)
    customer = models.OneToOneField("Customer",blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        # 使用电子邮件地址识别用户
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # 用户是否有特定权限
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # 用户是否有权限查看某个应用
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"