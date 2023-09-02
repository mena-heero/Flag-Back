from .base import *


DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://flagedu.com",
]

try:
    from .local import *
except ImportError:
    pass
