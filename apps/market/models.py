from django.contrib.auth.models import User
from andweb.django.models import models, BaseModel
from . import settings


class Category(BaseModel):
    name = models.CharField('名称', max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name='父类别', blank=True, null=True, related_name='children')
    order = models.IntegerField('顺序', default=0)

    def __str__(self):
        return self.name


class ImageFile(BaseModel):
    __slots__ = ()
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128)

    @property
    def url(self):
        return '/{0}/{1}'.format(settings.UPLOAD_URL, self.name)

    @property
    def path(self):
        return '{0}/{1}'.format(settings.UPLOAD_ROOT, self.name)

    def __str__(self):
        return self.name


class UserInfo(BaseModel):
    user = models.OneToOneField(User)
    nickname = models.CharField('昵称', max_length=32)
    fullname = models.CharField('姓名', max_length=32)
    phone = models.CharField('电话', max_length=11)
    qq = models.CharField('QQ', max_length=16)
    avatar = models.ForeignKey(ImageFile, verbose_name='头像', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Goods(BaseModel):
    VERIFY  = 0
    ONSALE  = 1
    SOLDOUT = 2
    NOTPASS = 3
    SUPPLY  = 0
    DEMAND  = 1

    STATUS = (
        (VERIFY,  '审核中'),
        (ONSALE,  '上架'),
        (SOLDOUT, '下架'),
        (NOTPASS,  '未通过'),
    )
    SDTYPE = (
        (SUPPLY, '转让'),
        (DEMAND, '求购'),
    )

    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简介', max_length=512, blank=True)
    desc_detail = models.CharField('详细描述', max_length=512, blank=True, default='')
    price = models.IntegerField('价格', default=0)
    location = models.CharField('地址', max_length=32)
    phone = models.CharField('电话', max_length=11)
    category = models.ForeignKey(Category, verbose_name='分类')
    images = models.ManyToManyField(ImageFile, verbose_name='图片')
    sdtype = models.SmallIntegerField("供求", default=SUPPLY, choices=SDTYPE)
    status = models.SmallIntegerField("状态", default=VERIFY, choices=STATUS)
    seller = models.ForeignKey(User, verbose_name='卖家')
    createtime = models.DateTimeField(auto_now_add=True)
    view_count    = models.IntegerField(default=0)
    # comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def firstimg(self):
        url = getattr(self, '_firstimg', None)
        if url is None:
            self._firstimg = url = self.images.first().url
        return url

    def otherimg(self):
        return (img.url for img in self.images.all()[1:])

    @classmethod
    def publics(cls):
        return cls.objects.filter(status=cls.ONSALE)


class Comment(BaseModel):
    goods = models.ForeignKey(Goods)
    user = models.ForeignKey(User)
    content = models.CharField(max_length=256)
    createtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class InstationMessage(BaseModel):
    receiver = models.ForeignKey(User, related_name='receiver')
    sender = models.ForeignKey(User, related_name='sender')
    content = models.CharField(max_length=255)
    sendtime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content


class RecommentGoods(BaseModel):
    goods = models.OneToOneField(Goods, verbose_name='商品')
    order = models.IntegerField('顺序', default=0)

    def __str__(self):
        return self.goods.name


class Carousel(BaseModel):
    img = models.CharField('图片', max_length=128)
    url = models.CharField('链接', max_length=128, null=True)
    h1  = models.CharField('主标题', max_length=64, null=True)
    h2  = models.CharField('副标题', max_length=64, null=True)
    order = models.IntegerField('顺序', default=0)

    def __str__(self):
        return self.goods.name


class NavCategory(BaseModel):
    category = models.OneToOneField(Category, verbose_name='分类')

    def __str__(self):
        return self.category.name


class Advert(BaseModel):
    class Meta:
        abstract = True

    img = models.CharField('图片', max_length=128)
    url = models.CharField('链接', max_length=128)
    title = models.CharField('标题', max_length=64)
    order = models.IntegerField('顺序', default=0)

    def __str__(self):
        return self.url


class IndexAdvert(Advert):
    pass


class FooterAdvert(Advert):
    pass


class ListBanner(Advert):
    pass