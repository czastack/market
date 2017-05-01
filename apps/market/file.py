from .basehandler import BaseHandler
from . import models, forms
from .. import settings
import os
import datetime


class DefaultHandler(BaseHandler):
    __slots__ = ()

    def upload(self):
        if self.is_post:
            file = self.request.FILES['file']
            file.name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + file.name[file.name.rfind('.'):]
            imgfile = models.ImageFile.objects.create(user=self.user, name=file.name)
            with open(imgfile.path, 'wb+') as fp:
                for chunk in file.chunks():
                    fp.write(chunk)
        
        return self.json({"files": [self.get_file_dict(imgfile, file.size)]})

    def delete(self):
        if self.request.method == 'DELETE':
            files = models.ImageFile.objects.filter(id=self.get_arg('id'), user=self.user)
            imgfile = files.first()
            if imgfile:
                files.delete()
                if not models.ImageFile.objects.filter(name=imgfile.name).exists():
                    os.remove(imgfile.path)
                return self.json({"files": [
                    {
                        imgfile.name: True
                    },
                ]})
        return ''


    @staticmethod
    def get_file_dict(imgfile, size=0):
        return {
            "name": imgfile.name,
            "size": size or os.path.getsize(imgfile.path),
            "url": imgfile.url,
            "thumbnailUrl": imgfile.url,
            "deleteUrl": __class__.guessUrl('delete?id=%d' % imgfile.id),
            "deleteType": "DELETE",
            "id": imgfile.id,
        }