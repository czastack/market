from ..basehandler import BaseHandler
from .. import models


class DefaultHandler(BaseHandler):
    __slots__ = ()

    pagetitle = '最热商品'

    def oninit(self):
        super().oninit()
        if not self.user.is_staff:
            return self.render('manage/denied')

    def hotest(self):
        data = models.Goods.objects.order_by('-view_count')[:10]
        return self.render(data=data)