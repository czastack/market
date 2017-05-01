from .basehandler import BaseHandler
from .. import models, forms


class DefaultHandler(BaseHandler):
    __slots__ = ()

    model = models.Goods
    pagetitle = '商品管理'

    def queryset(self):
        return models.Goods.objects.order_by('-createtime')

    def verify(self):
        if self.is_get:
            goods = self.get_or_404(models.Goods, id=self.get_arg('id'))
            status = self.get_arg('status')
            goods.status = status
            goods.save()

        return self.goback()

    