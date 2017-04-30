from ..basehandler import BaseHandler
from .. import models, settings

class BaseHandler(BaseHandler):

    def oninit(self):
        super().oninit()
        self.assign_common_data()

    def assign_common_data(self):
        if self.is_get:
            self.assign('navcats', [item.category for item in models.NavCategory.objects.filter(category__parent=None)])
            self.assign('footeradvert', models.FooterAdvert.objects.all())