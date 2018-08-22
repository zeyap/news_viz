from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jd2($-03+uvuc)m)zqh#1@mh+tyc!+m(28hij-gbzon3a(jk@l'

API_KEY = 'AIzaSyBth5uhNWogGsZT9LbT6pvXaUkSR1BwwWM'
CX_CODE = '017050252471438770433:cygqcpwrs7c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ELASTICSEARCH_DSL={
    'default': {
        'hosts': '66.42.102.161:9200'
    },
}