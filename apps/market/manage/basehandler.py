from ..basehandler import BaseHandler as _BaseHandler
from django.db import models


class BaseHandler(_BaseHandler):
    __slots__ = ()

    _template_dir = 'manage/base'

    def oninit(self):
        super().oninit()
        if not self.user.is_staff:
            return self.render('manage/denied')

    def index(self):
        data = self.queryset()
        return self.render(
            self.template_name('index', False),
            data=data,
            enable_edit=hasattr(self, 'form'),
            enable_delete=getattr(self, 'enable_delete', True)
        )

    def queryset(self):
        return self.model.objects.all()

    def add(self):
        if self.is_get:
            form = self.form()
        else:
            form = self.form(self.request.POST)
            if form.is_valid():
                form.save()
                return self.INDEX
        return self.render(form=form)

    def update(self):
        instance = self.model.objects.filter(id=self.get_arg('id')).first()
        if instance:
            if self.is_get:
                form = self.form(instance=instance, is_update=True)
            else:
                form = self.form(self.request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    return self.INDEX
            return self.render(form=form)
        else:
            return self.page404()

    def delete(self):
        self.model.objects.filter(id=self.get_arg('id')).delete()
        return self.INDEX