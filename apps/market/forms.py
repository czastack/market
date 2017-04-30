from andweb.django.formlib import forms, MyForm, bs_model_form as model_form, BS_CLASS
from . import models

UserForm  = model_form(models.User, fields=('username', 'email', 'password'), meta_attrs={
    'widgets': {'password': forms.PasswordInput},
})
UserInfoForm  = model_form(models.UserInfo, exclude=('user', 'avatar'))
CommentForm  = model_form(models.Comment, fields=('content',))
GoodsForm  = model_form(models.Goods, exclude=('seller', 'createtime', 'status', 'view_count', 'comment_count'), meta_attrs={
    'widgets': {
        'desc': forms.Textarea(attrs={"rows": 4}),
        'desc_detail': forms.Textarea,
        'sdtype': forms.RadioSelect,
    },
})


class LoginForm(MyForm):
    common_class = BS_CLASS
    username = forms.CharField(label='用户名或邮箱', required=True)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput)


class ForgetpwdForm(MyForm):
    common_class = BS_CLASS
    email = forms.CharField(label='邮箱', required=True)


class ChangepwdForm(MyForm):
    common_class = BS_CLASS
    curpassword = forms.CharField(label='当前密码', required=True, widget=forms.PasswordInput)
    password = forms.CharField(label='新密码', required=True, widget=forms.PasswordInput)
