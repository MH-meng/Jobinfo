from django import forms
from django.forms import fields
from django.forms import widgets


class StudentForm(forms.Form):
    number = fields.IntegerField(
        label="用户账户：",
        required=True,
        error_messages={
            'required': '*用户账户不能为空',
            'invalid': '*用户输入格式错误，必须为数字',
        },
        widget=widgets.TextInput(attrs={'class': 'form-control color', 'id': 'exampleInputEmail1'}),
        # 定制HTML插件, attrs 设置属性
    )
    pwd = fields.CharField(
        label="密码：",
        required=True,
        error_messages={
            'required': '*密码不能为空',
        },
        widget=forms.PasswordInput(attrs={'class': 'form-control color', 'id': 'exampleInputPassword1'})

    )
