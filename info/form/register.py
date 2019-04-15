from info import models
from django import forms
from django.forms import fields
from django.forms import widgets


class StudentRegisterForm(forms.Form):
    name = fields.CharField(
        label="企业名称：",
        required=True,
        min_length=2,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'用户名最少2个字节'
        },
        widget = widgets.TextInput(attrs={
            'class': 'form-control',
            'id': 'exampleInputNmae',
            'placeholder':'请输入企业名称'
        }),  # 定制HTML插件, attrs 设置属性
    )
    number = fields.CharField(
        label="企业账户：",
        required=True,
        max_length=11,
        min_length=11,
        error_messages={
            'required': '*用户账户不能为空',
            'max_length': '*用户账户最长为11位',
            'min_length': '*用户账户最短为11位',
            'invalid': '*用户输入格式错误，必须为数字',
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'id':'exampleInputNumber',
            'placeholder': '请输入企业账户，建议使用11位手机号码'
        }),  # 定制HTML插件, attrs 设置属性
    )
    pwd = fields.IntegerField(
        label="密码：",
        required=True,
        error_messages={
            'required': '*密码不能为空',
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'exampleInputPassword1',
            'placeholder': '请输入密码'
        })

    )


class RegisterForm(forms.Form):
    name = fields.CharField(
        label="学生姓名：",
        required=True,
        min_length=2,
        error_messages={
            'required': '学生姓名不能为空',
            'min_length': '学生姓名最少2个字节'
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'id': 'exampleInputNmae',
            'placeholder': '请输入学生姓名'
        }),  # 定制HTML插件, attrs 设置属性
    )
    number = fields.CharField(
        label="学生账户：",
        required=True,
        max_length=11,
        min_length=11,
        error_messages={
            'required': '*学生账户不能为空',
            'max_length': '*学生账户最长为11位',
            'min_length': '*学生账户最短为11位',
            'invalid': '*学生输入格式错误，必须为数字',
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'id': 'exampleInputNumber',
            'placeholder': '请输入学生账户，建议使用11位手机号码'
        }),  # 定制HTML插件, attrs 设置属性
    )
    pwd = fields.IntegerField(
        label="密码：",
        required=True,
        error_messages={
            'required': '*密码不能为空',
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'exampleInputPassword1',
            'placeholder': '请输入密码'
        })

    )
