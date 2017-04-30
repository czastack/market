from andweb.django.handler import BaseHandler

class DefaultHandler(BaseHandler):
    def index(self):
        return self.redirect('/market/index/')