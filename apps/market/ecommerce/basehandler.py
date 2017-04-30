from ..basehandler import BaseHandler
from .. import models, settings

class BaseHandler(BaseHandler):

    def oninit(self):
        super().oninit()
        if self.is_get:
            self.assign('navcats', [item.category for item in models.NavCategory.objects.filter(category__parent=None)])
            self.assign('footeradvert', models.FooterAdvert.objects.all())