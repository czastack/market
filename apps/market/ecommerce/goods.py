from .basehandler import BaseHandler
from ..file import DefaultHandler as FileHandler
from .. import models, forms, settings
from andweb.utils import cacheclassproperty
from django.db.models import Q
import json


class DefaultHandler(BaseHandler):
    __slots__ = ()

    def oninit(self):
        super().oninit()
        if self.is_get:
            self.assign('cats', models.Category.objects.filter(parent=None))

    def list(self):
        if self.is_get:
            args = self.get_args_adv(('search', ('cat', int, 0), 
                ('page', int, 1), ('limit', int, 0), 'order_by', 'order'), '')
            search = args.search
            cat = args.cat
            query = Q()
            if search:
                query |= Q(name__icontains=search) | Q(desc__icontains=search)
            if cat:
                query &= Q(category_id=cat) | Q(category__parent_id=cat)
            data = models.Goods.publics().filter(query)
            if args.order_by:
                if args.order == 'DESC':
                    args.order_by = '-' + args.order_by
                data = data.order_by(args.order_by)
            data, pagination = self.pagination(data, args.page, args.limit)
            hots = models.Goods.publics().order_by('-view_count')[:3]
            return self.render(
                data=data,
                args=args,
                catid=cat,
                hots=hots,
                pagination=pagination)

    def publish(self):
        if self.is_get:
            form = forms.GoodsForm()
            if self.userinfo:
                form.initial = {'phone': self.userinfo.phone}
                catid = self.get_arg('cat', None)
                if catid:
                    form.initial['category'] = catid
            del form.fields['images']
        else:
            form = forms.GoodsForm(self.request.POST)
            if form.is_valid():
                form.instance.seller = self.user
                form.instance.status = models.Goods.VERIFY
                form.save()
                return self.redirect('../account/goods')

        return self.render(form=form, upload_url=self.upload_url)

    def update(self):
        goods = models.Goods.objects.filter(id=self.get_arg('id'), seller=self.user).first()
        if goods:
            if self.is_get:
                form = forms.GoodsForm(instance=goods, is_update=True)
                del form.fields['images']
            else:
                form = forms.GoodsForm(self.request.POST, instance=goods, is_update=True)
                if form.is_valid():
                    form.instance.status = models.Goods.VERIFY
                    form.save()
                    return self.redirect('../account/goods')

            images = {"files": [FileHandler.get_file_dict(img) for img in goods.images.all()]}
            iamges = json.dumps(images)
            return self.render(
                form=form,
                upload_url=self.upload_url,
                images=iamges
            )
        else:
            return self.page404()

    def detail(self):
        if self.is_get:
            goods = models.Goods.objects.filter(id=self.get_arg('id')).first()
            if goods:
                similar = models.Goods.objects.filter(category=goods.category).exclude(id=goods.id)
                hots = models.Goods.objects.exclude(id=goods.id).order_by('-view_count')[:6]
                goods.view_count += 1
                goods.save()
                return self.render(goods=goods, similar=similar, hots=hots)
        return self.page404()

    def delete(self):
        models.Goods.objects.filter(id=self.get_arg('id'), seller=self.user).delete()
        return self.goback()

    def comment(self):
        if self.is_get:
            return self.render()
        else:
            pass

    @cacheclassproperty
    def upload_url(self):
        return FileHandler.guessUrl('upload')