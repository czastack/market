from .basehandler import BaseHandler
from .. import models, forms
from django.contrib import auth


class DefaultHandler(BaseHandler):
    __slots__ = ()

    def index(self):
        return self.redirect('setting')

    def setting(self, infoform=None, pwdform=None):
        if not infoform:
            infoform = forms.UserInfoForm(instance=self.userinfo)
        if not pwdform:
            pwdform = forms.ChangepwdForm()

        return self.render(self.template_name('setting'), infoform=infoform, pwdform=pwdform)
    
    def info(self):
        if self.is_post:
            form = forms.UserInfoForm(self.request.POST, instance=self.userinfo)
            if not self.userinfo:
                form.instance.user = self.user
            if form.is_valid():
                form.save()
                return self.redirect('setting')
        return self.setting(infoform=form)

    def avatar(self):
        if self.is_post:
            file = self.request.FILES['avatar']
            file.name = 'avatar-{0}{1}'.format(self.user.id, file.name[file.name.rfind('.'):])
            imgfile = models.ImageFile.objects.create(user=self.user, name=file.name)
            with open(imgfile.path, 'wb+') as fp:
                for chunk in file.chunks():
                    fp.write(chunk)
            info = self.userinfo
            if info:
                if info.avatar:
                    info.avatar.delete()
                info.avatar = imgfile
                info.save()
        return self.redirect('setting')

    def password(self):
        if self.is_get:
            form = None
        else:
            form = forms.ChangepwdForm(self.request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if self.user.check_password(data['curpassword']):
                    self.user.set_password(data['password'])
                    self.user.save()
                    auth.login(self.request, self.user)
                    self.redirect('setting')
                else:
                    form.errors['password'] = '您的旧密码不正确'
        return self.setting(pwdform=form)

    def goods(self):
        data = models.Goods.objects.filter(seller=self.user)
        return self.render(data=data)