from .basehandler import BaseHandler
from .. import models, forms


class DefaultHandler(BaseHandler):
    __slots__ = ()

    model = models.User
    pagetitle = '用户'

    def enable(self):
        if self.is_get:
            return self.render()
        else:
            pass


    def disable(self):
        if self.is_get:
            return self.render()
        else:
            pass
