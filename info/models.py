from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, null=True, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Tag(models.Model):
    """
    分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, unique=True)  # 分类名

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 文章标题
    desc = models.CharField(max_length=255)  # 文章描述
    status = models.CharField(max_length=1)  # 状态 0表示下架 1 表示提交 2表示浮动
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    tags = models.ForeignKey(to="Tag", to_field="nid", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Float(models.Model):
    """
    浮动表
    """
    nid = models.AutoField(primary_key=True)
    f_title = models.CharField(max_length=10)  # 浮动标题
    a_title = models.CharField(max_length=50)  # 浮动标题
    a_desc = models.CharField(max_length=255)  # 文章描述
    f_desc = models.CharField(max_length=30)  # 浮动简介
    status = models.CharField(max_length=1)  # 状态 0表示禁止浮动 1 表示浮动
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间


    class Meta:
        verbose_name = "浮动表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.f_title


class Invite(models.Model):
    """招聘会"""
    i_name = models.CharField(max_length=32,verbose_name='标题', blank=True, null=True)
    i_data = models.DateTimeField(verbose_name='招聘时间', blank=True, null=True)
    i_city = models.CharField(verbose_name='招聘城市', max_length=36, blank=True, null=True)
    i_sponsor = models.CharField(verbose_name='招聘主办方', max_length=36, blank=True, null=True)
    i_type = models.CharField(max_length=1, verbose_name='招聘类型', blank=True, null=True)
    i_content = models.TextField(verbose_name='招聘会内容', max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name_plural = '招聘会表'

    def __str__(self):
        return self.i_name



class Conpanys(models.Model):
    """企业"""
    c_name = models.CharField(verbose_name='公司名称', max_length=64)
    c_number = models.CharField(verbose_name='账号', max_length=11)
    c_pwd = models.CharField(max_length=64, verbose_name='密码')
    c_nature = models.CharField(verbose_name='企业性质', max_length=64, blank=True, null=True)
    c_city = models.CharField(verbose_name='所在地区', max_length=36, blank=True, null=True)
    c_industry = models.CharField(verbose_name='所属行业', max_length=64, blank=True, null=True)
    c_scale = models.IntegerField(verbose_name='企业规模', blank=True, null=True, default=0)
    c_phone = models.CharField(verbose_name='电话', max_length=11, blank=True, null=True)
    c_linkman = models.CharField(verbose_name='法人代表', max_length=12, blank=True, null=True)
    c_create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True)
    c_type = models.CharField(verbose_name='企业类型', max_length=64, blank=True, null=True)
    c_site = models.CharField(verbose_name='详细地址', max_length=64, blank=True, null=True)
    c_time = models.CharField(verbose_name='注册时间', max_length=64, blank=True, null=True)
    c_capital = models.CharField(verbose_name='注册资本', max_length=64, blank=True, null=True)
    c_manage = models.CharField(verbose_name='经营范围', max_length=255, blank=True, null=True)
    c_business = models.CharField(verbose_name='营业执照', max_length=100, blank=True, null=True)
    c_brief = models.TextField(verbose_name='企业简介', max_length=1000, blank=True, null=True)
    class Meta:
        verbose_name_plural = '企业表'

    def __str__(self):
        return self.c_name


class Teachin(models.Model):
    """宣讲会"""
    x_title = models.CharField(verbose_name='宣讲标题',max_length=36, blank=True, null=True)
    x_time = models.DateTimeField(verbose_name='宣讲时间', blank=True, null=True)
    x_city = models.CharField(verbose_name='宣讲城市',max_length=36, blank=True, null=True)
    x_school = models.CharField(verbose_name='宣讲学校',max_length=36, blank=True, null=True)
    x_detail = models.TextField(verbose_name='宣讲会详情', blank=True, null=True)
    x_status = models.CharField(max_length=1, verbose_name='宣讲会状态', default="0")  # 0表示待审核 1表示审核通过 2表示审核未通过
    x_company = models.ForeignKey(Conpanys, null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = '宣讲会表'

    def __str__(self):
        return self.x_title


class Zhaopin(models.Model):
    """招聘"""
    z_position = models.CharField(verbose_name='招聘职位名称', max_length=64, blank=True, null=True)
    z_number = models.IntegerField(verbose_name='招聘人数', blank=True, null=True)
    z_salary = models.CharField(verbose_name='月薪', max_length=64,blank=True, null=True)
    z_education = models.CharField(verbose_name='学历要求', max_length=64, blank=True, null=True)
    z_experience = models.CharField(verbose_name='岗位要求', max_length=500, blank=True, null=True)
    z_nature = models.CharField(max_length=1, verbose_name='招聘类型', blank=True, null=True)
    z_data = models.DateTimeField(verbose_name='面试时间', blank=True, null=True)
    z_city = models.CharField(verbose_name='面试地点', max_length=36, blank=True, null=True)
    z_email = models.EmailField(verbose_name='投递邮箱', blank=True, null=True)
    z_detail = models.TextField(verbose_name='招聘会详情', blank=True, null=True)
    z_company = models.ForeignKey(Conpanys, null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name_plural = '招聘信息表'

    def __str__(self):
        return self.z_position