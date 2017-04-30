from .basehandler import BaseHandler
from .. import models, forms


class DefaultHandler(BaseHandler):
    __slots__ = ()

    model = models.Category
    form  = forms.model_form(model)

