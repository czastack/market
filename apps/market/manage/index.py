from .basehandler import BaseHandler
from .. import models


class DefaultHandler(BaseHandler):
    __slots__ = ()

    def index(self):
        goods = models.Goods.objects
        return self.render('manage/index', 
            goodscount = goods.count(),
            toverify = goods.filter(status=models.Goods.VERIFY).count(),
            usercount = models.User.objects.count(),
        )
