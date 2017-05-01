from andweb.django.handler import AssignableHandler
from django.contrib import auth
from .ecommerce.basehandler import BaseHandler 
from . import models, forms
import math


class DefaultHandler(AssignableHandler):
    __slots__ = ()
    _template_dir = 'ecommerce'

    
    def oninit(self):
        super().oninit()
        self.assign_common_data()            
    
    oninit_appdata = BaseHandler.oninit_appdata
    logined = BaseHandler.logined
    assign_common_data = BaseHandler.assign_common_data

    def oninit_appdata(self, data):
        data['MANAGEURL'] = data['APPURL'] + 'manage/'

    def index(self):
        recomments = models.RecommentGoods.objects.order_by('order')[:10]
        recomments = (item.goods for item in recomments)
        goods = models.Goods.publics().order_by('-createtime')[:12]
        count = math.ceil(goods.count() / 2)
        three = goods[:count]
        two = goods[count:count+count]
        index_advert = models.IndexAdvert.objects.order_by('-order')[:5]
        footer_advert = models.FooterAdvert.objects.order_by('-order')[:5]
        cats = models.Category.objects.filter(parent=None)

        return self.render(
            recomments=recomments,
            three=three,
            two=two,
            index_advert=index_advert,
            footer_advert=footer_advert,
            cats=cats,
        )

    def _login_success(self, user):
        auth.login(self.request, user)
        self.session['user'] = user.username
        return self.redirect(self.session.pop('refer', 'index'))

    def register(self):
        if self.is_get:
            form = forms.UserForm()
        else:
            form = forms.UserForm(self.request.POST)
            if form.is_valid():
                user = form.instance
                if models.User.objects.filter(username=user.username).exists():
                    form.errors['username'] = ['用户名已存在']
                elif models.User.objects.filter(email=user.email).exists():
                    form.errors['email'] = ['邮箱已被注册']
                else:
                    user.set_password(user.password)
                    user.save()
                    return self._login_success(user)

        return self.render(form=form)

    def login(self):
        if self.is_get:
            next_ = self.get_arg('next', None)
            if next_ == '':
                next_ = self.referer
            if next_:
                self.session.setdefault('refer', next_)
            form = forms.LoginForm()
        else:
            form = forms.LoginForm(self.request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = auth.authenticate(username=data['username'], password=data['password'])

                if not user:
                    try:
                        user = models.User.objects.get(email=data['username'])
                        if not user.check_password(data['password']):
                            user = None
                    except models.User.DoesNotExist:
                        pass

                if user:
                    if user.is_active:
                        # 登录成功
                        return self._login_success(user)
                    else:
                        err = '您的账户已被禁用'
                else:
                    err = '用户名或密码错误'
                form.errors['username'] = [err]
        return self.render(form=form)

    def logout(self):
        auth.logout(self.request)
        return self.redirect('login')

    def forgetpwd(self):
        if self.is_get:
            form = forms.ForgetpwdForm()
        else:
            form = forms.ForgetpwdForm(self.request.POST)
        return self.render(form=form)
