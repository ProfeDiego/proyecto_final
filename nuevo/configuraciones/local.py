from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'diego.e.var@gmail.com'
# EMAIL_HOST_PASSWORD = 'Pcdiegopc3108'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'diego.e.var@gmail.com'