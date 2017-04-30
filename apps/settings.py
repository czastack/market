from andweb.django.settings import *

SECRET_KEY = 'kz9kh2^0*gbl(r1^6rn74&8&ew17f00j^(xscqg7&u*!v%)%c5'

INSTALLED_APPS += [
    'apps.market',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'market',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'',
        'PORT':''
    }
}