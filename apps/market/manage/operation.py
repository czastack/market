from .basehandler import BaseHandler
from .. import models, forms
from ..file import DefaultHandler as FileHandler


class NavcatHandler(BaseHandler):
    __slots__ = ()
    model = models.NavCategory
    pagetitle = '导航栏分类'

    def index(self, form=None):
        checkedids = [item['category_id'] for item in self.model.objects.values('category_id')]
        cats = models.Category.objects.order_by('order', 'id').all()
        for cat in cats:
            if cat.id in checkedids:
                cat.checked = True
        return self.render(self.template_name('index', False), data=cats)

    def add(self):
        if self.is_post:
            ids = self.request.POST.getlist('id')
            self.model.objects.filter().delete()
            for id_ in ids:
                self.model.objects.create(category_id=id_)
        return self.goback()


class CarouselHandler(BaseHandler):
    __slots__ = ()
    pagetitle = '首页百叶窗'
    model = models.Carousel
    form  = forms.model_form(model)


class RecommentHandler(BaseHandler):
    __slots__ = ()
    model = models.RecommentGoods
    form  = forms.model_form(model)
    pagetitle = '首页推荐商品'

    def queryset(self):
        return self.model.objects.order_by('order')


class IndexadvertHandler(BaseHandler):
    __slots__ = ()
    model = models.IndexAdvert
    form  = forms.model_form(model)
    pagetitle = '首页广告列表'


class FooteradvertHandler(BaseHandler):
    __slots__ = ()
    model = models.FooterAdvert
    form  = forms.model_form(model)
    pagetitle = '底部广告列表'


class ListbannerHandler(BaseHandler):
    __slots__ = ()
    model = models.ListBanner
    form  = forms.model_form(model)
    pagetitle = '列表页Banner'


class UploadimgHandler(BaseHandler.__bases__[0]):
    __slots__ = ()

    def index(self):
        if self.is_get:
            return self.render(upload_url=FileHandler.guessUrl('upload'))