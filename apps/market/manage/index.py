from .basehandler import BaseHandler


class DefaultHandler(BaseHandler):
    __slots__ = ()

    def index(self):
        return self.render('manage/index')
