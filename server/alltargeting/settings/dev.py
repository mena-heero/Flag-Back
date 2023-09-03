from .base import *
from decouple import config


DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://dev.flagedu.com",
    "https://flagedu.com",
    "http://localhost",
    "http://127.0.0.1",
]


try:
    from .local import *
except ImportError:
    pass
