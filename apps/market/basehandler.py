#encoding: utf8

from andweb.django.handler import AssignableHandler
# from django.contrib.auth.decorators import login_required
from . import models, settings

class BaseHandler(AssignableHandler):

    def oninit(self):
        result = super().oninit()
        if result:
            return result

        if not self.logined:
            # 记录当前路径以便登录后跳转
            self.session['refer'] = self.request.path
            return self.redirect(self.url('login', True))

    def oninit_appdata(self, data):
        data['MANAGEURL'] = data['APPURL'] + 'manage/'

    def page404(self):
        return self.render(self.route[1] + '/page404')

    def pagination(self, data, cur, limit=None):
        num = len(data)
        # 防止传递limit=0
        limit = limit or settings.PAGE_LIMIT
        total = num // limit + (num % limit > 0)
        pages = range(total)[cur-3 if cur-3 >=0 else 0: cur+3 if cur+3 <= total else total]
        pages = [x+1 for x in pages]
        if 1 not in pages:
            pages = ([1] if 2 in pages else [1, '...']) + pages
        if total not in pages:
            pages = pages + ([total] if (total - 1) in pages else ['...', total])
        skip = (cur - 1) * limit
        if data:
            data = data[skip:skip+limit]
        end = min(num, skip + limit)
        return data, self.render(self.route[1] + '/pagination', 
            num=num,
            cur=cur,
            total=total,
            pages=pages,
            start=skip + 1,
            end=end,
            prev=cur-1,
            next=cur+1 if cur is not total else 0,
        )

    @property
    def logined(self):
        return self.user.is_authenticated()

    @property
    def userinfo(self):
        try:
            return self.user.userinfo
        except:
            return None